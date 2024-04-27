from typing import Tuple
from pathlib import Path
from uuid import uuid4
import aiohttp
from fastapi import FastAPI, Depends, Cookie, HTTPException
from aiohttp_client_cache import CachedSession, FileBackend  # type: ignore
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles


cache = FileBackend(
    use_temp=True,
    expire_after=2 * 43200,  # 24 hours
)

base_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
BUILD_PATH = Path(__file__).parent / "build"


sessions = {}


async def wp_get_cookies(username: str, password: str) -> dict:
    """Retrieves authorization cookies from Wattpad by logging in with user creds.

    Args:
        username (str): Username.
        password (str): Password.

    Raises:
        ValueError: Bad status code.
        ValueError: No cookies returned.

    Returns:
        dict: Authorization cookies.
    """
    async with CachedSession(headers=base_headers) as session:
        async with session.post(
            "https://www.wattpad.com/auth/login?nextUrl=%2F&_data=routes%2Fauth%2Flogin",
            data={
                "username": username.lower(),
                "password": password,
            },  # the username.lower() is for caching
        ) as response:
            if response.status != 204:
                raise ValueError("Not a 204.")

            cookies = {
                k: v.value
                for k, v in response.cookies.items()  # Thanks https://stackoverflow.com/a/32281245
            }

            if not cookies:
                raise ValueError("No cookies.")

            return cookies


async def wp_get_inbox(authorization: dict, username: str) -> Tuple[list, int, list]:
    """Retrieves all users in Inbox.

    Args:
        authorization (dict): Authorization cookies.
        username (str): Username of logged in user.

    Returns:
        Tuple[list, int, list]: Parsed data, the total number of threads, and the raw API data.
    """

    url = f"https://www.wattpad.com/api/v3/users/{username}/inbox?filter=&limit=20&offset=0"

    threads = []
    total = 0
    raw_data = []

    headers = base_headers.copy()

    async with aiohttp.ClientSession(
        headers=headers, cookies=authorization
    ) as session:  # No caching
        while url:
            async with session.get(url) as response:
                response.raise_for_status()

                data = await response.json()
                if data.get("nextUrl"):
                    url = data["nextUrl"]
                else:
                    url = ""

                total = data["total"]
                threads = threads + data["threads"]
                raw_data.append(data)

    return (threads, total, raw_data)


async def wp_get_messages(
    authorization: dict, username: str, inbox_user: str
) -> Tuple[list, int, list]:
    """Retrieves all messages between the logged in User and provided User.

    Args:
        authorization (dict): Authorization cookies.
        username (str): Username of logged in user.
        inbox_user (str): Username of other user in thread.

    Returns:
        Tuple[list, int, list]: Parsed data, the total number of messages, and the raw API data.
    """

    url = f"https://www.wattpad.com/api/v3/users/{username}/inbox/{inbox_user}?offset=0"

    messages = []
    total = 0
    raw_data = []

    headers = base_headers.copy()

    async with aiohttp.ClientSession(
        headers=headers, cookies=authorization
    ) as session:  # No caching
        while url:
            async with session.get(url) as response:
                response.raise_for_status()

                data = await response.json()
                if data.get("nextUrl"):
                    url = data["nextUrl"]
                else:
                    url = ""

                total = data["total"]
                messages.append(data["messages"])
                raw_data.append(data)

    return messages, total, raw_data


app = FastAPI()


@app.get("/")
def home():
    return FileResponse(BUILD_PATH / "index.html")


@app.get("/list")
def home():
    return FileResponse(BUILD_PATH / "list.html")


@app.get("/login")
async def login(username: str, password: str):
    """Login and return cookies.

    Args:
        username (str): Username.
        password (str): Password.

    Raises:
        HTTPException: Invalid Credentials or Processing Error (ratelimited).

    Returns:
        RedirectResponse: Redirects to homepage with session authorization cookie.
    """
    response = RedirectResponse("/list")
    username = username.lower()

    uid = str(uuid4())

    try:
        cookies = await wp_get_cookies(username, password)
    except ValueError:
        raise HTTPException(
            status_code=403,
            detail="Incorrect credentials. If you're confident they are correct, please join the discord.",
        )
    sessions[uid] = {"cookies": cookies, "uid": uid, "username": username}

    response.set_cookie("authorization", uid)
    return response


def cookie_dep(authorization: str = Cookie(None)):
    """Protect authorized-only paths by checking for session cookie.

    Args:
        authorization (str): Session token.

    Raises:
        HTTPException: Not authorized.

    Returns:
        dict: Session data.
    """
    if not authorization or not authorization in sessions:
        raise HTTPException(
            status_code=403, detail="Not authorized, please login first."
        )

    return sessions[authorization]


@app.get("/inbox")
async def get_inbox(session_data: dict = Depends(cookie_dep)):
    """Retrieve all messages in Inbox."""
    return await wp_get_inbox(session_data["cookies"], session_data["username"])


@app.get("/messages")
async def get_messages(usernames: str, session_data: dict = Depends(cookie_dep)):
    """Retrieve all messages in a Thread between the logged in user, and each user in the provided CSV list of usernames."""
    usernames_to_fetch = usernames.lower().split(",")
    to_return = {}

    if not usernames_to_fetch:
        return {}

    for username in usernames_to_fetch:
        to_return[username] = await wp_get_messages(
            session_data["cookies"], session_data["username"], username
        )

    return to_return


@app.get("/logout")
def logout():
    """Delete authorization cookie if it exists."""
    response = RedirectResponse("/")
    response.set_cookie("authorization", "")
    return response


app.mount("/", StaticFiles(directory=BUILD_PATH), "static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)

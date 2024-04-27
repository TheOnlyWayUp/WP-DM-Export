# Wattpad DM Export [[Link]](https://export.towu.dev)
---
Wattpad is [deleting](https://support.wattpad.com/hc/articles/204412040-Private-messages) all DMs on May 6th 2024. This WebApp implements an export solution.

Export [here](https://export.towu.dev).

Join the [discord](https://discord.gg/TfDY8G67Ss)!

![](/images/home.png)

![](/images/users.png)

![](/images/chat.png)



HTML Rendering could be improved, but the JSON Export works without issue. Authentication data is cached for 24 hours to prevent ratelimits. I've tried to make this very easy to self-host, so please do.

If you need support, join the [discord](https://discord.gg/TfDY8G67Ss)!

Stars ⭐ are appreciated. Thanks!

## Self Hosting Guide
1. Clone the repository: `git clone https://github.com/TheOnlyWayUp/WP-DM-Export && cd WP-DM-Export`
2. Build the image: `docker build . -t 'wp_dm_export'` (This takes about 2 Minutes)
3. Run the Container: `docker run -d -p 5043:80 wp_dm_export`

That's it! You can use your instance at `http://localhost:5043`. API Documentation is available at `http://localhost:5043/docs`.

## Contributing

If you're interested in helping, I'd really appreciate PRs improving [HTML Rendering](https://github.com/TheOnlyWayUp/WP-DM-Export/blob/0ee014e3800bda7b5d7a112e86446b4bb6d474d0/src/Frontend/src/routes/list/%2Bpage.svelte#L54-L121). This is being tracked in #2.

---

My other projects:
- WattpadDownloader: Visit [here](https://wpd.rambhat.la). Download Wattpad books as EPUBs in seconds!
- Wattpad-Py: Visit [here](https://documentation.rambhat.la). Python package to interface with Wattpad's Data API.

---

<div align="center">
    <p>TheOnlyWayUp © 2024</p>
</div>

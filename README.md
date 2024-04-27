# Wattpad DM Export
---
Export Wattpad DMs.

Wattpad is [deleting](https://support.wattpad.com/hc/articles/204412040-Private-messages) all DMs on May 6th 2024. This WebApp implements an export solution.

![](/images/home.png)

![](/images/users.png)

![](/images/chat.png)



It's by no means perfect (especially the HTML rendering), but allows you to get your data out. You can download your DM Data as HTML or JSON. This enables you to use the data in your code, or just view it locally as you would on Wattpad's Inbox page.

Stars ⭐ are appreciated. Thanks!

## Self Hosting Guide
1. Clone the repository: `git clone https://github.com/TheOnlyWayUp/WP-DM-Export && cd WP-DM-Export`
2. Build the image: `docker build . -t 'wp_dm_export'` (This takes about 2 Minutes)
3. Run the Container: `docker run -d -p 5043:80 wp_dm_export`

That's it! You can use your instance at `http://localhost:5043`. API Documentation is available at `http://localhost:5043/docs`.

---

<div align="center">
    <p>TheOnlyWayUp © 2024</p>
</div>

<script>
	import '../app.pcss';
	export const prerender = true;
</script>

<div role="alert" class="alert alert-warning fixed">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		class="stroke-info h-6 w-6 shrink-0"
		><path
			stroke-linecap="round"
			stroke-linejoin="round"
			stroke-width="2"
			d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
		></path></svg
	>
	<span class="font-bold"
		>Want to download Wattpad Stories? <span class="font-normal">
			Visit <a
				href="https://wpd.rambhat.la"
				target="_blank"
				data-umami-event="WPD"
				class="link text-xl">WattpadDownloader</a
			>
		</span></span
	>
</div>

<slot></slot>

<footer class="footer footer-center bg-base-300 text-base-content fixed bottom-0 p-4">
	<aside>
		<div class="grid w-full max-w-lg grid-cols-3">
			<a
				href="https://liberapay.com/TheOnlyWayUp/"
				target="_blank"
				class="link"
				data-umami-event="Footer Donate">Donate</a
			>
			<a href="https://rambhat.la" target="_blank" class="link" data-umami-event="Footer AboutMe"
				>About Me</a
			>
			<a
				href="https://discord.gg/TfDY8G67Ss"
				target="_blank"
				class="link"
				data-umami-event="Footer Discord">Discord</a
			>
		</div>
		<!-- <p>
			Copyright © 2024 - All rights reserved by <a
				href="https://rambhat.la"
				class="link"
				target="_blank"
				data-umami-event="CopyrightHolder">Dhanush R</a
			>
		</p> -->
		<button data-feedback-fish class="link pb-2" data-umami-event="Feedback">Feedback</button>
	</aside>
</footer>

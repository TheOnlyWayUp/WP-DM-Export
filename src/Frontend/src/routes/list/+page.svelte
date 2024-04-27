<script lang="ts">
	import { onMount } from 'svelte';
	export const prerender = true;

	let threads = [];
	let selected_users = {};

	onMount(async (e) => {
		let response = await fetch('/inbox');
		let r_threads = await response.json();

		r_threads[0].forEach((record) => {
			selected_users[record.user.name] = false;
		});
		threads = r_threads[0];
		console.log(threads);
	});

	function downloadObjectAsJson(exportObj, exportName) {
		// Thanks https://stackoverflow.com/a/30800715
		var dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(exportObj));
		var downloadAnchorNode = document.createElement('a');
		downloadAnchorNode.setAttribute('href', dataStr);
		downloadAnchorNode.setAttribute('download', exportName + '.json');
		document.body.appendChild(downloadAnchorNode); // required for firefox
		downloadAnchorNode.click();
		downloadAnchorNode.remove();
	}

	function downloadObjectAsHTML(exportObj, exportName) {
		// Thanks https://stackoverflow.com/a/30800715
		var dataStr = 'data:text/html;charset=utf-8,' + exportObj;
		var downloadAnchorNode = document.createElement('a');
		downloadAnchorNode.setAttribute('href', dataStr);
		downloadAnchorNode.setAttribute('download', exportName + '.html');
		document.body.appendChild(downloadAnchorNode); // required for firefox
		downloadAnchorNode.click();
		downloadAnchorNode.remove();
	}

	let responses = {};

	async function download() {
		Object.keys(selected_users).forEach(async (username) => {
			if (selected_users[username]) {
				let response = await fetch('/messages?usernames=' + username);
				let data = await response.json();
				responses[username] = data[username.toLowerCase()];
				console.log('fetched', username, responses, data);
			}
		});
	}

	function generate_html(username) {
		let tailwind_import = '<script src="https://cdn.tailwindcss.com"></' + 'script' + '>';
		let template = `<html>
<head>
<title>Conversation with ${username}</title>
${tailwind_import}
</head>
<body class="bg-slate-300">`;

		let sent = `
<div class="w-screen my-3 place-items-end grid">
<div class="grid-cols-2 grid w-fit place-items-center">
<div class="flex flex-col text-right max-w-md">
<p class="text-slate-650 ">{username}</p>
<p class="bg-slate-100 p-2 rounded-lg max-w-md text-wrap rounded-tr-none ">{content}</p>
<p class="text-slate-500">{date}</p>
</div>
<img src="{avatar}" alt="{username}'s Display Picture" class="rounded-full w-[48px] h-[48px]">
</div>`;

		let received = `
<div class="w-screen my-3">
<div class="grid-cols-2 grid w-fit place-items-center">
<img src="{avatar}" alt="{username}'s Display Picture" class="rounded-full w-[48px] h-[48px]">
<div class="flex flex-col max-w-md">
<p class="text-slate-650">{username}</p>
<p class="bg-slate-100 p-2 rounded-lg max-w-md text-wrap rounded-tl-none">{content}</p>
<p class="text-slate-500">{date}</p>
</div>
</div>
`;
		let end = `</body>
</html>`;

		let content = '';
		let data = responses[username][0];

		let messages = [];
		data.forEach((api_data) => {
			api_data.forEach((message) => {
				messages.push(message);
			});
		});

		content = content + template;
		messages.reverse().forEach((message) => {
			if (message.from.name.toLowerCase() == username.toLowerCase()) {
				content =
					content +
					received
						.replaceAll('{username}', message.from.name)
						.replaceAll('{content}', message.body)
						.replaceAll('{date}', message.createDate)
						.replaceAll('{avatar}', message.from.avatar);
			} else {
				content =
					content +
					sent
						.replaceAll('{username}', message.from.name)
						.replaceAll('{content}', message.body)
						.replaceAll('{date}', message.createDate)
						.replaceAll('{avatar}', message.from.avatar);
			}
		});

		content = content + end;

		return content;
	}
</script>

<div class="hero bg-base-200 min-h-screen">
	<div class="hero-content text-center">
		<div class="max-w-md">
			<h1 class="text-5xl font-bold">Select Users</h1>
			<p class="py-6">
				<label class="form-control w-full max-w-xs">
					<div class="label">
						<span class="label-text text-lg">Which users should be exported?</span>
					</div>
					<div class="grid max-h-64 w-fit overflow-y-auto rounded-md">
						{#each threads as thread}
							<div class="flex flex-row place-items-center space-x-2 rounded-md bg-white p-4">
								<div class="avatar">
									<div
										class="ring-primary ring-offset-base-100 w-12 rounded-full ring ring-offset-2"
									>
										<img src={thread.user.avatar} />
									</div>
								</div>
								<span class="label-text text-xl">{thread.user.name}</span>
								<input
									type="checkbox"
									class="toggle"
									bind:checked={selected_users[thread.user.name]}
								/>
								{#key responses}
									{#if responses[thread.user.name]}
										<div class="py-2">
											<button
												class="link"
												on:click={(e) => {
													downloadObjectAsHTML(generate_html(thread.user.name), thread.user.name);
												}}
												data-umami-event="HTML Download">Download</button
											>
											<button
												class="link text-sm"
												on:click={(e) => {
													let data = responses[thread.user.name][0];
													let messages = [];
													data.forEach((api_data) => {
														api_data.forEach((message) => {
															messages.push(message);
														});
													});
													downloadObjectAsJson(messages, thread.user.name);
												}}
												data-umami-event="JSON Download">(or Raw)</button
											>
										</div>
									{/if}
								{/key}
							</div>
						{/each}
					</div>
				</label>
			</p>
			<div class="z-10 grid max-w-lg grid-cols-3 space-x-5">
				<button
					class="btn btn-ghost btn-outline"
					on:click={(e) => {
						Object.keys(selected_users).forEach((username) => {
							selected_users[username] = true;
						});
					}}>Select All</button
				>
				<button
					class="btn btn-primary"
					on:click={async (e) => {
						await download();
					}}
					data-umami-event="Continue"
					onclick="AfterDownloadModal.showModal()">Continue</button
				>
				<button
					class="btn btn-ghost btn-outline"
					on:click={(e) => {
						Object.keys(selected_users).forEach((username) => {
							selected_users[username] = false;
						});
					}}>Deselect All</button
				>
			</div>
		</div>
	</div>
</div>

<dialog id="AfterDownloadModal" class="modal">
	<div class="modal-box">
		<h3 class="text-lg font-bold">Your download has started</h3>
		<div class="space-y-2 py-4">
			<p class="text-xl">
				Hi, thanks for using my site! If you found it useful, please consider <a
					href="https://liberapay.com/TheOnlyWayUp/"
					target="_blank"
					class="link"
					data-umami-event="Donate">donating</a
				> to keep this project alive.
			</p>
			<p>
				You can also join us on <a
					href="https://discord.gg/P9RHC4KCwd"
					target="_blank"
					class="link"
					data-umami-event="Discord">discord</a
				>, where we discuss updates and features.
			</p>
			<p class="text-lg">
				Please take a look at <a href="https://rambhat.la" class="link" data-umami-event="My Work"
					>my work</a
				>!
			</p>
		</div>
		<div class="pt-2">
			<form method="dialog">
				<!-- if there is a button in form, it will close the modal -->
				<button class="btn btn-sm btn-ghost w-full" data-umami-event="AfterDownloadModal Close"
					>Close</button
				>
			</form>
		</div>
	</div>
</dialog>

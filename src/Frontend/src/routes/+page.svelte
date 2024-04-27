<div class="hero bg-base-200 min-h-screen">
	<div class="hero-content flex-col lg:flex-row-reverse">
		<div class="m-5 text-center lg:text-left">
			<h1
				class="bg-gradient-to-r from-red-700 via-yellow-600 to-pink-600 bg-clip-text text-5xl text-5xl font-bold font-extrabold text-transparent"
			>
				Wattpad DM Exporter
			</h1>
			<p class="max-w-md py-6">
				On <span class="underline">May 6th, 2024</span>, Wattpad plans to remove the DM feature and
				completely delete all related data. This is an unofficial export program.
			</p>
			<button
				class="btn btn-ghost btn-outline"
				on:click={(e) => {
					window.location.replace('/logout');
				}}
				data-umami-event="Logout">Log Out</button
			>
			<a
				class="btn btn-ghost btn-outline mx-5"
				href="https://github.com/TheOnlyWayUp"
				target="_blank"
				data-umami-event="Logout">Source Code</a
			>
		</div>

		<div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
			<form class="card-body" method="GET" action="/login">
				<div class="form-control">
					<label class="label" for="username">
						<span class="label-text">Email or Username</span>
					</label>
					<input
						type="text"
						placeholder="email or username"
						class="input input-bordered"
						name="username"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label" for="password">
						<span class="label-text">Password</span>
					</label>
					<input
						type="password"
						placeholder="password"
						class="input input-bordered"
						name="password"
						required
					/>
				</div>
				<div class="form-control mt-6">
					<button class="btn btn-primary" data-umami-event="Login">Login</button>
				</div>
			</form>
		</div>
	</div>
</div>

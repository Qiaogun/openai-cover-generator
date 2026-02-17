export default {
  async fetch(request, env) {
    // Serve all static files from the repository root via Workers Assets.
    // This makes `wrangler deploy` (workers.dev) show the same frontend as Pages.
    return env.ASSETS.fetch(request);
  },
};

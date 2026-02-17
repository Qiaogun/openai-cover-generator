export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1) Try exact static asset path first.
    let response = await env.ASSETS.fetch(request);
    if (response.status !== 404) return response;

    // 2) Directory-style route => /path/index.html
    if (url.pathname.endsWith('/')) {
      response = await env.ASSETS.fetch(new Request(new URL(`${url.pathname}index.html`, url), request));
      if (response.status !== 404) return response;
    }

    // 3) Extension-less route => /path.html
    if (!url.pathname.includes('.')) {
      response = await env.ASSETS.fetch(new Request(new URL(`${url.pathname}.html`, url), request));
      if (response.status !== 404) return response;
    }

    // 4) Final fallback to app entry file.
    return env.ASSETS.fetch(new Request(new URL('/index.html', url), request));
  },
};

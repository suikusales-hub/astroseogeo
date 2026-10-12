const CANONICAL_HOST = 'seogeo.cc';
const PAGES_DEV_SUFFIX = '.pages.dev';
const ROUTE_MANIFEST_PATH = '/site-routes.json';

let cachedRoutes;

async function loadRoutes(request, env) {
  if (cachedRoutes) {
    return cachedRoutes;
  }

  const manifestUrl = new URL(ROUTE_MANIFEST_PATH, request.url);
  const response = await env.ASSETS.fetch(new Request(manifestUrl.toString(), { method: 'GET' }));

  if (!response.ok) {
    cachedRoutes = new Set(['/']);
    return cachedRoutes;
  }

  const manifest = await response.json();
  cachedRoutes = new Set(Array.isArray(manifest.routes) ? manifest.routes : ['/']);
  return cachedRoutes;
}

function hasFileExtension(pathname) {
  return /\/[^/]+\.[a-z0-9_]+$/i.test(pathname);
}

function toExtensionlessPath(pathname) {
  if (pathname === '/index.html') {
    return '/';
  }

  return pathname.replace(/\.html$/i, '') || '/';
}

async function serveNotFound(request, env) {
  const notFoundUrl = new URL('/404.html', request.url);
  const response = await env.ASSETS.fetch(new Request(notFoundUrl.toString(), { method: 'GET' }));

  if (!response.ok) {
    return new Response('404 Not Found', {
      status: 404,
      headers: {
        'content-type': 'text/plain; charset=utf-8',
        'x-robots-tag': 'noindex',
      },
    });
  }

  const headers = new Headers(response.headers);
  headers.set('x-robots-tag', 'noindex');
  headers.set('cache-control', 'public, max-age=60');

  return new Response(response.body, {
    status: 404,
    statusText: 'Not Found',
    headers,
  });
}

async function serveAssetOrNotFound(request, env) {
  const response = await env.ASSETS.fetch(request);
  const pathname = new URL(request.url).pathname;
  const contentType = response.headers.get('content-type') || '';

  if (response.status === 404 || (hasFileExtension(pathname) && !pathname.endsWith('.html') && contentType.includes('text/html'))) {
    return serveNotFound(request, env);
  }

  return response;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.hostname.endsWith(PAGES_DEV_SUFFIX)) {
      url.protocol = 'https:';
      url.hostname = CANONICAL_HOST;
      url.port = '';

      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname !== '/' && url.pathname.endsWith('/')) {
      url.pathname = url.pathname.replace(/\/+$/, '');
      return Response.redirect(url.toString(), 301);
    }

    // Serve the Sveltia CMS admin SPA deterministically, bypassing the
    // directory-index redirect behavior of the asset server.
    if (url.pathname === '/admin' || url.pathname === '/admin/') {
      url.pathname = '/admin/index.html';
      return env.ASSETS.fetch(new Request(url.toString(), request));
    }

    const routes = await loadRoutes(request, env);

    if (url.pathname === '/404' || url.pathname === '/404.html') {
      return serveNotFound(request, env);
    }

    if (url.pathname.endsWith('.html')) {
      const extensionlessPath = toExtensionlessPath(url.pathname);
      if (routes.has(extensionlessPath)) {
        url.pathname = extensionlessPath;
        return Response.redirect(url.toString(), 301);
      }

      return serveNotFound(request, env);
    }

    if (hasFileExtension(url.pathname)) {
      return serveAssetOrNotFound(request, env);
    }

    if (!routes.has(url.pathname)) {
      return serveNotFound(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};

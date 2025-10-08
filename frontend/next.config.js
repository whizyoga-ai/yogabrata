/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Disable API rewrites for static export
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: 'https://api.yogabrata.com/api/:path*',
  //     },
  //   ]
  // },
}

module.exports = nextConfig

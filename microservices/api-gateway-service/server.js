/**
 * API Gateway Service for Yogabrata Microservices
 * Routes requests to appropriate microservices with load balancing and authentication
 */

const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const winston = require('winston');
const jwt = require('jsonwebtoken');
require('dotenv').config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 8080;

// Configure Winston logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'api-gateway' },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ],
});

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS ? process.env.ALLOWED_ORIGINS.split(',') : ['http://localhost:3000', 'http://localhost:3001'],
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // limit each IP to 1000 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});
app.use(limiter);

// Request logging middleware
app.use((req, res, next) => {
  logger.info('Incoming request', {
    method: req.method,
    url: req.url,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  });
  next();
});

// Authentication middleware (optional)
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return next(); // No token provided, continue without authentication
  }

  jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key', (err, user) => {
    if (err) {
      logger.warn('Invalid token', { error: err.message });
      return next(); // Invalid token, continue without authentication
    }
    req.user = user;
    next();
  });
};

// Service URLs from environment variables
const SERVICES = {
  startupFormation: process.env.STARTUP_FORMATION_SERVICE_URL || 'http://startup-formation:8000',
  legalCompliance: process.env.LEGAL_COMPLIANCE_SERVICE_URL || 'http://legal-compliance:8000',
  contentStrategy: process.env.CONTENT_STRATEGY_SERVICE_URL || 'http://content-strategy:8000',
  businessFormation: process.env.BUSINESS_FORMATION_SERVICE_URL || 'http://business-formation:8000',
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-gateway',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Service discovery endpoint
app.get('/api/services', (req, res) => {
  res.json({
    services: Object.keys(SERVICES).map(key => ({
      name: key,
      url: SERVICES[key],
      status: 'healthy' // In production, implement actual health checks
    }))
  });
});

// Route to Startup Formation Service
app.use('/api/v1/startup', authenticateToken, createProxyMiddleware({
  target: SERVICES.startupFormation,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/startup': '/api/v1'
  },
  onError: (err, req, res) => {
    logger.error('Startup Formation Service error', { error: err.message, url: req.url });
    res.status(500).json({
      error: 'STARTUP_FORMATION_ERROR',
      message: 'Startup Formation Service is currently unavailable'
    });
  },
  onProxyReq: (proxyReq, req, res) => {
    logger.info('Proxying to Startup Formation', { url: req.url });
  }
}));

// Route to Legal Compliance Service
app.use('/api/v1/legal', authenticateToken, createProxyMiddleware({
  target: SERVICES.legalCompliance,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/legal': '/api/v1'
  },
  onError: (err, req, res) => {
    logger.error('Legal Compliance Service error', { error: err.message, url: req.url });
    res.status(500).json({
      error: 'LEGAL_COMPLIANCE_ERROR',
      message: 'Legal Compliance Service is currently unavailable'
    });
  }
}));

// Route to Content Strategy Service
app.use('/api/v1/content', authenticateToken, createProxyMiddleware({
  target: SERVICES.contentStrategy,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/content': '/api/v1'
  },
  onError: (err, req, res) => {
    logger.error('Content Strategy Service error', { error: err.message, url: req.url });
    res.status(500).json({
      error: 'CONTENT_STRATEGY_ERROR',
      message: 'Content Strategy Service is currently unavailable'
    });
  }
}));

// Route to Business Formation Service
app.use('/api/v1/business', authenticateToken, createProxyMiddleware({
  target: SERVICES.businessFormation,
  changeOrigin: true,
  pathRewrite: {
    '^/api/v1/business': '/api/v1'
  },
  onError: (err, req, res) => {
    logger.error('Business Formation Service error', { error: err.message, url: req.url });
    res.status(500).json({
      error: 'BUSINESS_FORMATION_ERROR',
      message: 'Business Formation Service is currently unavailable'
    });
  }
}));

// Fallback route for unmatched API paths
app.use('/api/*', (req, res) => {
  res.status(404).json({
    error: 'API_ENDPOINT_NOT_FOUND',
    message: `API endpoint ${req.originalUrl} not found`,
    availableServices: Object.keys(SERVICES)
  });
});

// Serve static files for frontend (development fallback)
if (process.env.NODE_ENV === 'development') {
  app.use(express.static('public'));

  // Catch all handler for SPA
  app.get('*', (req, res) => {
    res.sendFile('index.html', { root: 'public' });
  });
}

// Global error handler
app.use((err, req, res, next) => {
  logger.error('Unhandled error', { error: err.message, stack: err.stack });
  res.status(500).json({
    error: 'INTERNAL_ERROR',
    message: 'An unexpected error occurred'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'NOT_FOUND',
    message: `Route ${req.originalUrl} not found`
  });
});

// Graceful shutdown handling
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully');
  process.exit(0);
});

// Start server
app.listen(PORT, () => {
  logger.info(`API Gateway started on port ${PORT}`);
  logger.info('Available service routes:', Object.keys(SERVICES));
});

module.exports = app;

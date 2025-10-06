'use client'

import { useState } from 'react'

interface Service {
  id: number
  title: string
  description: string
  icon: string
  agent: string
  mcp_sources: string[]
  estimated_time: string
}

const services: Service[] = [
  {
    id: 1,
    title: "Launch Start-up",
    description: "AI-powered business formation guidance with Washington State compliance focus",
    icon: "🚀",
    agent: "Business Formation Agent",
    mcp_sources: ["WA DOR", "WA SOS", "Legal Compliance"],
    estimated_time: "15-30 min"
  },
  {
    id: 2,
    title: "Content Moderation & Promotions",
    description: "Automated content review and promotional strategy optimization",
    icon: "📝",
    agent: "Content Strategy Agent",
    mcp_sources: ["Market Data", "Social APIs"],
    estimated_time: "10-20 min"
  },
  {
    id: 3,
    title: "Hire & Fire AI Bots / Robots",
    description: "Intelligent automation setup and workforce management guidance",
    icon: "🤖",
    agent: "Automation Agent",
    mcp_sources: ["HR Compliance", "Tech Standards"],
    estimated_time: "20-40 min"
  },
  {
    id: 4,
    title: "Legal Compliance Assistant",
    description: "Real-time legal compliance checking and regulatory guidance",
    icon: "⚖️",
    agent: "Legal Compliance Agent",
    mcp_sources: ["Federal Legal", "State Regulations"],
    estimated_time: "10-25 min"
  },
  {
    id: 5,
    title: "Market Research & Intelligence",
    description: "AI-powered market analysis and competitive intelligence gathering",
    icon: "💼",
    agent: "Market Intelligence Agent",
    mcp_sources: ["Industry Data", "Market Trends"],
    estimated_time: "15-30 min"
  },
  {
    id: 6,
    title: "Automated Tax & Accounting Setup",
    description: "Intelligent tax registration and accounting system configuration",
    icon: "💰",
    agent: "Tax Compliance Agent",
    mcp_sources: ["WA DOR", "IRS Data", "Tax Regulations"],
    estimated_time: "20-35 min"
  },
  {
    id: 7,
    title: "Intellectual Property Protection",
    description: "AI-assisted trademark and patent research and filing guidance",
    icon: "🛡️",
    agent: "IP Protection Agent",
    mcp_sources: ["USPTO", "WIPO", "Legal Databases"],
    estimated_time: "25-45 min"
  },
  {
    id: 8,
    title: "Grant & Funding Finder",
    description: "Automated grant matching and funding opportunity identification",
    icon: "🎯",
    agent: "Funding Agent",
    mcp_sources: ["Grants.gov", "SBA Data", "Private Funding"],
    estimated_time: "15-30 min"
  }
]

export default function Home() {
  const [selectedService, setSelectedService] = useState<Service | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [aiResponse, setAiResponse] = useState<string>('')

  const handleServiceClick = async (service: Service) => {
    setSelectedService(service)
    setIsLoading(true)
    setAiResponse('')

    try {
      // Call the AI agent API
      const response = await fetch(`http://localhost:8000/api/v2/agents/business_formation/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task: `Help me with ${service.title}: ${service.description}`,
          user_id: 'web_user',
          priority: 1
        })
      })

      if (response.ok) {
        const data = await response.json()
        setAiResponse(data.message || 'Service response received')
      } else {
        setAiResponse('Service temporarily unavailable. Please try again later.')
      }
    } catch (error) {
      setAiResponse('Unable to connect to AI service. Please ensure the backend is running.')
    }

    setIsLoading(false)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-indigo-900">
      {/* Header */}
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Yogabrata AI Platform
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Multi-Service AI Platform with MCP Integration for Intelligent Business Services
          </p>
          <div className="mt-4 flex justify-center items-center space-x-2">
            <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
            <span className="text-sm text-gray-500 dark:text-gray-400">AI Agents Active</span>
          </div>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
          {services.map((service) => (
            <div
              key={service.id}
              onClick={() => handleServiceClick(service)}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1 border border-gray-200 dark:border-gray-700"
            >
              <div className="p-6">
                <div className="text-4xl mb-4">{service.icon}</div>
                <h3 className="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-200">
                  {service.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3">
                  {service.description}
                </p>
                <div className="space-y-2">
                  <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                    <span className="font-medium">Agent:</span>
                    <span className="ml-1">{service.agent}</span>
                  </div>
                  <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                    <span className="font-medium">Time:</span>
                    <span className="ml-1">{service.estimated_time}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* AI Response Panel */}
        {selectedService && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200">
                {selectedService.icon} {selectedService.title}
              </h2>
              <button
                onClick={() => setSelectedService(null)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                ✕
              </button>
            </div>

            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="ml-3 text-gray-600 dark:text-gray-400">
                  Consulting AI Agent...
                </span>
              </div>
            ) : (
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {selectedService.agent} Response
                  </span>
                </div>
                <p className="text-gray-800 dark:text-gray-200">
                  {aiResponse || 'Click on a service to get AI-powered assistance.'}
                </p>
                <div className="mt-3 text-xs text-gray-500 dark:text-gray-400">
                  MCP Sources: {selectedService.mcp_sources.join(', ')}
                </div>
              </div>
            )}
          </div>
        )}

        {/* API Status */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center space-x-4 bg-white dark:bg-gray-800 rounded-lg px-6 py-3 shadow-lg">
            <div className="flex items-center">
              <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
              <span className="text-sm text-gray-600 dark:text-gray-400">Backend API</span>
            </div>
            <div className="flex items-center">
              <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
              <span className="text-sm text-gray-600 dark:text-gray-400">MCP Servers</span>
            </div>
            <div className="flex items-center">
              <span className="w-3 h-3 bg-purple-500 rounded-full mr-2"></span>
              <span className="text-sm text-gray-600 dark:text-gray-400">AI Agents</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

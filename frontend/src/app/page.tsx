"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import { useTheme } from "next-themes";
import {
  Brain,
  Sun,
  Moon,
  Menu,
  X,
  Search,
  TrendingUp,
  FileText,
  Shield,
  Zap,
  Globe,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

export default function LandingPage() {
  const { theme, setTheme } = useTheme();
  const darkMode = theme === "dark";
  const targetRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: targetRef, offset: ["0 1", "1.33 1"] });
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "-20%"]);

  const scrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  const features = [
    {
      icon: <TrendingUp className="w-8 h-8 text-blue-500" />,
      title: "IQVIA Insights Agent",
      desc: "Real-time market analysis with trends, CAGR calculations, and competitive mapping.",
    },
    {
      icon: <Shield className="w-8 h-8 text-emerald-500" />,
      title: "Patent Landscape Agent",
      desc: "Comprehensive IP analysis from global databases with expiry timelines.",
    },
    {
      icon: <Search className="w-8 h-8 text-purple-500" />,
      title: "Clinical Trials Agent",
      desc: "Pipeline intelligence from ClinicalTrials.gov with sponsor insights.",
    },
    {
      icon: <Globe className="w-8 h-8 text-indigo-500" />,
      title: "Web Intelligence Agent",
      desc: "Scans guidelines, publications, and forums with source verification.",
    },
    {
      icon: <Zap className="w-8 h-8 text-amber-500" />,
      title: "EXIM Trends Agent",
      desc: "Import-export analytics for APIs and formulations across global markets.",
    },
    {
      icon: <FileText className="w-8 h-8 text-pink-500" />,
      title: "Report Generator Agent",
      desc: "PDF reports with charts, tables, and actionable insights.",
    },
  ];

  return (
    <div className="relative min-h-screen bg-background text-foreground transition-colors duration-500">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 w-full z-50 backdrop-blur-xl border-b border-border bg-background/70">
        <div className="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="bg-gradient-to-tr from-blue-500 to-indigo-500 w-10 h-10 rounded-xl flex items-center justify-center shadow-md">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-xl">Synthera</span>
          </div>

          <div className="hidden md:flex items-center gap-6">
            <button onClick={() => scrollTo("features")} className="hover:text-blue-500 transition">
              Features
            </button>
            <button onClick={() => scrollTo("contact")} className="hover:text-blue-500 transition">
              Contact
            </button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(darkMode ? "light" : "dark")}
              aria-label="Toggle theme"
            >
              {darkMode ? <Sun /> : <Moon />}
            </Button>
            <Button variant="outline" onClick={() => (window.location.href = "/login")}>
              Sign In
            </Button>
            <Button onClick={() => (window.location.href = "/signup")} className="bg-blue-600 text-white">
              Sign Up
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section ref={targetRef} className="pt-32 pb-24 relative overflow-hidden">
        <motion.div
          style={{ y }}
          className="absolute inset-0 bg-gradient-to-b from-blue-50 via-indigo-50 to-white dark:from-gray-900 dark:via-gray-950 dark:to-gray-900"
        />
        <div className="max-w-7xl mx-auto relative z-10 px-6 grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-block px-4 py-2 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200 mb-6">
              Accelerating Pharmaceutical Innovation
            </div>
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Transform Drug Discovery with{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-500">
                Agentic AI
              </span>
            </h1>
            <p className="text-lg text-muted-foreground mb-8">
              AI-powered patent analysis, market forecasting, and drug repurposing—accelerating
              innovation like never before.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-lg rounded-lg" onClick={() => (window.location.href = "/signup")}>
                Get Started
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1 }}
            className="relative bg-white/50 dark:bg-gray-800/30 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-gray-200/30 dark:border-gray-700/30"
          >
            <div className="space-y-5">
              {[
                { icon: <Search className="text-blue-500" />, title: "Molecule Search", desc: "Finding candidate compounds for diabetes..." },
                { icon: <TrendingUp className="text-green-500" />, title: "Market Analysis", desc: "$45B market, 8.2% CAGR projected." },
                { icon: <FileText className="text-purple-500" />, title: "Reports Ready", desc: "15 viable opportunities identified." },
              ].map((box, i) => (
                <motion.div key={i} whileHover={{ scale: 1.05 }} className="bg-background rounded-xl p-4 shadow-lg border border-border">
                  <div className="flex items-center space-x-3 mb-2">
                    {box.icon}
                    <span className="font-semibold">{box.title}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{box.desc}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 bg-gradient-to-b from-transparent to-blue-50 dark:to-gray-900">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-4xl font-bold mb-4"
          >
            Intelligent Agent Ecosystem
          </motion.h2>
          <p className="text-lg text-muted-foreground mb-16">
            Specialized AI agents working together to accelerate your research pipeline.
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
            {features.map((f, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Card className="shadow-xl hover:-translate-y-2 hover:shadow-2xl transition-all border-border dark:bg-gray-800">
                  <CardContent className="p-6">
                    <div className="mb-4">{f.icon}</div>
                    <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
                    <p className="text-muted-foreground">{f.desc}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact */}
      <section id="contact" className="py-24">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-4">Get in Touch</h2>
          <p className="text-lg text-muted-foreground mb-10">
            Ready to revolutionize your R&D pipeline with Synthera AI?
          </p>
          <Card className="dark:bg-gray-800/60 backdrop-blur-xl border-border shadow-2xl">
            <CardContent className="space-y-6 p-8">
              <div className="grid md:grid-cols-2 gap-6">
                <Input placeholder="First Name" />
                <Input placeholder="Last Name" />
              </div>
              <Input placeholder="Email" type="email" />
              <Input placeholder="Company" />
              <Textarea placeholder="Message" rows={4} />
              <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">Send Message</Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-950 text-gray-400 py-12 text-center border-t border-gray-800">
        <div className="flex justify-center items-center space-x-2 mb-4">
          <div className="bg-blue-600 w-10 h-10 rounded-lg flex items-center justify-center">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold text-white">Synthera</span>
        </div>
        <p>Accelerating pharmaceutical innovation through intelligent AI agents</p>
        <p className="text-sm text-gray-500 mt-2">© 2025 Synthera. All rights reserved.</p>
      </footer>
    </div>
  );
}

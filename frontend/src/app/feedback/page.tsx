"use client";

import { useState } from "react";
import Link from "next/link";

type FeedbackType = "issue" | "idea" | "other";

export default function FeedbackPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [type, setType] = useState<FeedbackType>("issue");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error">(
    "idle"
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("sending");

    const subject = encodeURIComponent(
      `[BC Council Tracker] ${type === "issue" ? "Issue Report" : type === "idea" ? "Idea" : "Feedback"}: ${message.slice(0, 60)}`
    );
    const body = encodeURIComponent(
      `Name: ${name}\nEmail: ${email}\nType: ${type}\n\n${message}`
    );

    window.location.href = `mailto:nick@kairo.chat?subject=${subject}&body=${body}`;
    setStatus("sent");
  };

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/"
          className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
        >
          &larr; Back to Tracker
        </Link>
      </div>

      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold text-gray-900">
          Report Issues / Share Ideas
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Have a bug to report or an idea to improve the tracker? Fill out the
          form below and we&apos;ll get back to you.
        </p>

        {status === "sent" ? (
          <div className="mt-6 rounded-md bg-green-50 p-4">
            <p className="text-sm font-medium text-green-800">
              Your email client should have opened with the message pre-filled.
              If it didn&apos;t, you can email us directly at{" "}
              <a
                href="mailto:nick@kairo.chat"
                className="underline hover:text-green-900"
              >
                nick@kairo.chat
              </a>
              .
            </p>
            <button
              onClick={() => {
                setName("");
                setEmail("");
                setType("issue");
                setMessage("");
                setStatus("idle");
              }}
              className="mt-3 text-sm font-medium text-green-700 hover:text-green-900 hover:underline"
            >
              Submit another
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700"
              >
                Name
              </label>
              <input
                id="name"
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                placeholder="Your name"
              />
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label
                htmlFor="type"
                className="block text-sm font-medium text-gray-700"
              >
                Type
              </label>
              <select
                id="type"
                value={type}
                onChange={(e) => setType(e.target.value as FeedbackType)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
              >
                <option value="issue">Report an Issue</option>
                <option value="idea">Share an Idea</option>
                <option value="other">Other Feedback</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="message"
                className="block text-sm font-medium text-gray-700"
              >
                Message
              </label>
              <textarea
                id="message"
                required
                rows={5}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                placeholder={
                  type === "issue"
                    ? "Describe the issue you encountered..."
                    : type === "idea"
                      ? "Tell us about your idea..."
                      : "What's on your mind?"
                }
              />
            </div>

            <button
              type="submit"
              disabled={status === "sending"}
              className="w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none disabled:opacity-50"
            >
              {status === "sending" ? "Opening email..." : "Send Feedback"}
            </button>
          </form>
        )}
      </div>

      <div className="rounded-md bg-blue-50 p-4">
        <p className="text-sm text-blue-800">
          You can also reach us directly at{" "}
          <a
            href="mailto:nick@kairo.chat"
            className="font-medium underline hover:text-blue-900"
          >
            nick@kairo.chat
          </a>
        </p>
      </div>
    </div>
  );
}

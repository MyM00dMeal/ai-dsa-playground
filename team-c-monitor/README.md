# Team C – Real-Time AI API Monitoring & Anomaly Detection

A FastAPI + Streamlit system that monitors AI API usage in real time, computes rolling metrics, and detects anomalies using streaming data structures.

## Problem Statement

Modern AI APIs must be continuously monitored to ensure reliability, detect failures, and prevent abuse.
This project simulates a real-time monitoring system that ingests API logs, computes rolling usage metrics, and detects anomalous behavior such as error spikes, latency spikes, and per-user abuse.

## Learning Objectives

- Apply data structures and algorithms to real-world monitoring problems
- Design clean REST APIs using FastAPI
- Build an interactive monitoring dashboard using Streamlit
- Implement sliding window metrics on streaming data
- Practice professional Git workflows with branches and pull requests

## System Architecture

- **Backend (FastAPI):** Accepts log events and exposes metrics via REST APIs
- **Core Logic:** Implements sliding window aggregation, metrics computation, and anomaly detection
- **Frontend (Streamlit):** Displays real-time metrics, anomalies, and charts

## Core Algorithms & Data Structures

- **Sliding Window (deque):** Maintains recent log events efficiently
- **Hash Maps:** Aggregate per-user and global metrics
- **Statistics:** Mean and standard deviation for anomaly thresholds

## Anomaly Detection

Baseline metrics are computed over the sliding window.
An anomaly is detected when a metric exceeds:

mean + k × standard deviation

Severity levels:

- INFO: Slight deviation
- WARNING: Significant deviation
- CRITICAL: Severe abnormal behavior

## How to Run

pip install -r requirements.txt

# Backend

cd team-c-monitor/backend
uvicorn app.main:app --reload

# Frontend

cd team-c-monitor/frontend
streamlit run app.py

## Testing

Run unit tests using:
pytest

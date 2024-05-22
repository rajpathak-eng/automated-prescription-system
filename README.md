# Automated Prescription Download and Forwarding System

## Overview

This project automates the process of downloading prescription files from LensAdvisor and forwarding them to a supplier via email. It is designed for Chambora, an online eyewear store using Shopify, to streamline their prescription handling process.

## Problem Statement

Chambora faced challenges in managing prescription files manually, which involved:
1. Extracting prescription links from order confirmation emails.
2. Downloading prescription files from LensAdvisor.
3. Forwarding the files to their supplier with appropriate labels.

## Solution

The solution involves an automated system that:
1. Fetches order confirmation emails from specific senders.
2. Extracts prescription links from the emails.
3. Downloads the prescription files using LensAdvisor's API.
4. Forwards the files to the supplier, labeled with the order number and date.
5. Runs automatically at regular intervals using a cron job.

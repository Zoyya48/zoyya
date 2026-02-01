Smart Parking System – Full Stack Application

University Project – Data Structures & System Design

This project implements a Smart Parking Allocation and Zone Management System for Lahore city. It is a full-stack application that connects a professional animated frontend interface with a Python Flask backend designed using object-oriented programming and data structure concepts.

The system allows a user to select a vehicle, enter a registration number, choose a parking zone, view available slots, and confirm parking through backend allocation logic. The goal of this project is to demonstrate how theoretical concepts from data structures and system design can be applied to a real-world problem.

⸻

Project Overview

The project is divided into two major parts:

Frontend
The frontend is built using HTML, CSS, and JavaScript. It includes animated screens, smooth transitions, and a multi-step parking flow. The UI handles user interaction and communicates with the backend using HTTP requests.

Backend
The backend is built using Python and Flask. It manages zones, parking slots, vehicles, and parking requests. The backend applies allocation logic, tracks system state, and responds to frontend requests in real time.

⸻

Folder Structure

The project follows a clean and modular structure:
	•	app.py is the main Flask application and entry point
	•	templates folder contains the complete HTML user interface
	•	models folder contains object-oriented representations such as Zone, ParkingArea, ParkingSlot, Vehicle, and ParkingRequest
	•	core folder contains system logic including allocation handling, rollback support, and the main parking system controller
	•	requirements.txt lists Python dependencies

This separation ensures readability, maintainability, and clear responsibility of each file.

⸻

How the System Works (Data Flow)
	1.	The user opens the application in a browser
	2.	The frontend loads from Flask and requests zone data
	3.	The backend sends available zones and parking slots
	4.	The user selects a vehicle type and enters a registration number
	5.	The user selects a preferred parking zone
	6.	The backend allocation engine searches for an available slot
	7.	Slot preference is given to the selected zone
	8.	If the zone is full, allocation falls back to other zones
	9.	The backend updates slot state and confirms booking
	10.	The frontend displays a confirmation ticket to the user

This flow ensures smooth communication between frontend and backend while maintaining system consistency.

⸻

Parking Request Lifecycle

Each parking request follows a defined lifecycle:

REQUESTED → ALLOCATED → OCCUPIED

A request can also be cancelled, in which case rollback logic restores the previous state. This ensures proper state management and avoids data inconsistency.

⸻

Allocation Strategy

The allocation strategy works as follows:
	•	First, the system checks for available slots in the requested zone
	•	If the requested zone is full, it searches other zones
	•	The first available slot is allocated
	•	If no slots are available, the system returns a failure response

This approach simulates real-world parking overflow handling.

⸻

Data Structures Used

The backend applies core data structure concepts including:
	•	Lists to manage parking slots
	•	Dictionaries for fast lookup of zones and vehicles
	•	Stack-based logic for rollback operations
	•	State tracking to manage request transitions

These structures ensure efficient processing and system stability.

⸻

Features Implemented
	•	Zone-based parking management
	•	Real-time slot availability
	•	Multi-step booking flow
	•	Object-oriented backend design
	•	Cross-zone allocation support
	•	Rollback handling
	•	Animated and responsive frontend
	•	Clean modular code structure

⸻

Project Purpose

This project was developed as part of a university course to demonstrate:
	•	Practical use of data structures
	•	System design and modular programming
	•	Frontend and backend integration
	•	Real-world problem solving using software engineering principles

⸻

Repository Access

This repository is public and can be accessed, cloned, and run locally for evaluation. The project runs on a local Flask server and is fully functional when accessed through a browser.

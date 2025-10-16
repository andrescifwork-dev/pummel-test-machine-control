Pummel Test Machine
Short description This repository contains firmware and documentation for a pummel test machine intended strictly for testing and evaluation. This material is provided for test purposes only; each person or organization must design, build, and validate their own machine before real-world use. ⚠️

Scope of the code
What the code covers

⚙️ Main user configuration: test parameters, sequences, and savable settings.

🛠️ Stepper motor control: motion routines, positioning, and limit handling.

🔨 Strike sequence: logic to execute a predefined striking pattern that aims to cover the specimen area.

What the code does not cover / responsibility

🚫 Does not include full mechanical construction instructions, structural material specifications, or safety certifications.

🧑‍🔧 Each user is responsible for their own mechanical design, safety validation, testing, and regulatory compliance.

Repository structure
src/rpi_pico/ — Pico firmware (process control)

src/arduino/ — Arduino sketch (LCD menu and encoder)

src/motor_control/ — Stepper drivers and motion routines

hw/ — Electrical schematics and wiring diagrams

docs/ — Test procedure, flowchart, and calibration notes

img/ — Prototype photos and illustrative sequences

data/ — Example test result CSVs

Basic usage (development)
Set and save parameters via the LCD + encoder menu. 🔧

Verify limit switches and physical safety guards. ✅

Flash firmware to Raspberry Pi Pico and Arduino from the src/ folders. 💾

Run tests from the menu and store logs in data/. 📂

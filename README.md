# TuneX V0

TuneX V0 is a local desktop PID tuning and control-system experimentation tool built with Python.

It focuses on real-time simulation, live response visualization, iterative PID tuning, and engineering-focused workflow design.

TuneX is designed as the foundation for future embedded and robotics-oriented tuning systems.

---

## Features

* Real-time PID simulation
* Live response graph rendering
* Iterative tuning workflow
* Performance metrics:

  * Overshoot
  * Settling time
  * Rise time
  * Steady-state error
* Tuning history visualization
* Dark engineering-style UI
* Modular multi-file architecture
* Cross-platform desktop support

---

## Tech Stack

* Python
* PySide6
* PyQtGraph
* NumPy

---

## Architecture

```text
tunex/
├── core/
├── ui/
├── models/
└── utils/
```

The project follows a modular structure with clear separation between:

* simulation logic
* PID control
* metrics analysis
* UI rendering
* tuning workflow

---

## Current Version (V0)

TuneX V0 is an experimentation and simulation-focused release.

### Current Scope

* Simulated first-order system
* Desktop visualization
* Manual PID tuning workflow

### Planned Future Features

* Hardware telemetry
* ESP32/Pico integration
* Wireless tuning
* PlatformIO workflows
* AI-assisted tuning
* Robotics control applications

---

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## Screenshots

![TuneX Screenshot](assets/screenshot1.png)

---

## License

MIT License

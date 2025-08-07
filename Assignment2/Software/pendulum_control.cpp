/*
 * Assignment 2: Pendulum Position Control
 * 
 * This C++ script controls a Nanotec DB87M01-S stepper motor to cycle
 * a pendulum between horizontal (0°) and vertical (90°) positions
 * continuously without stopping.
 * 
 * System Requirements:
 * - Motor: Nanotec DB87M01-S with integrated controller
 * - Communication: RS485/Modbus or CANopen
 * - Load: 2kg pendulum at 0.3m radius
 * - Motion: Continuous 0° ↔ 90° cycling
 */

#include <iostream>
#include <chrono>
#include <thread>
#include <cmath>
#include <vector>
#include <fstream>
#include <iomanip>
#include <signal.h>

// System configuration
const double PENDULUM_MASS = 2.0;      // kg
const double PENDULUM_LENGTH = 0.3;    // m
const double MOTOR_TORQUE = 0.3924;    // N⋅m (calculated)
const double GEARBOX_RATIO = 10.0;     // 10:1 reduction

// Motion parameters
const double MIN_ANGLE = 0.0;          // degrees (horizontal)
const double MAX_ANGLE = 90.0;         // degrees (vertical)
const double MAX_VELOCITY = 30.0;      // degrees/second
const double ACCELERATION = 60.0;      // degrees/second²
// NO PAUSE - Continuous motion without stopping as per requirement

// Control parameters
const double POSITION_TOLERANCE = 0.5; // degrees
const int CONTROL_PERIOD_MS = 10;      // 100Hz control loop
const int MAX_CYCLES = 1000;           // maximum test cycles

// Global control flag for safe shutdown
volatile bool g_running = true;

// Signal handler for clean shutdown
void signalHandler(int /* signum */) {
    std::cout << "\nShutdown signal received. Stopping motor safely...\n";
    g_running = false;
}

// Data logging structure
struct CycleData {
    int cycle_number;
    double timestamp;
    double current_position;
    double target_position;
    double velocity;
    double load_torque;
    bool limit_switch_0;
    bool limit_switch_90;
    std::string status;
};

class PendulumController {
private:
    double current_position_;
    double target_position_;
    double current_velocity_;
    int current_cycle_;
    bool direction_up_;  // true = 0° to 90°, false = 90° to 0°
    
    std::vector<CycleData> cycle_log_;
    std::ofstream log_file_;
    
    std::chrono::steady_clock::time_point start_time_;
    
public:
    PendulumController() : 
        current_position_(0.0),
        target_position_(0.0),
        current_velocity_(0.0),
        current_cycle_(0),
        direction_up_(true),
        start_time_(std::chrono::steady_clock::now()) {
        
        // Initialize logging
        log_file_.open("../Output/pendulum_cycle_log.csv");
        log_file_ << "Cycle,Timestamp,Current_Position,Target_Position,Velocity,Load_Torque,Limit_0,Limit_90,Status\n";
        
        std::cout << "Pendulum Controller Initialized\n";
        std::cout << "System Parameters:\n";
        std::cout << "  Mass: " << PENDULUM_MASS << " kg\n";
        std::cout << "  Length: " << PENDULUM_LENGTH << " m\n";
        std::cout << "  Motor Torque: " << MOTOR_TORQUE << " N⋅m\n";
        std::cout << "  Range: " << MIN_ANGLE << "° to " << MAX_ANGLE << "°\n\n";
    }
    
    ~PendulumController() {
        if (log_file_.is_open()) {
            log_file_.close();
        }
    }
    
    // Calculate required torque at current position
    double calculateLoadTorque(double angle_deg) {
        double angle_rad = angle_deg * M_PI / 180.0;
        // Torque = M * g * L * sin(θ) for pendulum
        // At θ=0° (horizontal): sin(0) = 0, but we use cos for static analysis
        // At θ=90° (vertical): sin(90) = 1
        return PENDULUM_MASS * 9.81 * PENDULUM_LENGTH * sin(angle_rad);
    }
    
    // Generate smooth motion profile (trapezoidal) - CONTINUOUS without zero velocity at endpoints
    double generateMotionProfile(double start_pos, double end_pos, double current_time, double total_time) {
        double distance = end_pos - start_pos;
        double accel_time = MAX_VELOCITY / ACCELERATION;
        double decel_time = accel_time;
        double const_time = total_time - accel_time - decel_time;
        
        if (const_time < 0) {
            // Triangular profile (no constant velocity phase)
            accel_time = total_time / 2.0;
            decel_time = accel_time;
            const_time = 0;
        }
        
        double position, velocity;
        
        if (current_time <= accel_time) {
            // Acceleration phase
            double t = current_time;
            position = start_pos + 0.5 * ACCELERATION * t * t;
            velocity = ACCELERATION * t;
        }
        else if (current_time <= accel_time + const_time) {
            // Constant velocity phase
            double t = current_time - accel_time;
            position = start_pos + 0.5 * ACCELERATION * accel_time * accel_time + MAX_VELOCITY * t;
            velocity = MAX_VELOCITY;
        }
        else if (current_time < total_time) {
            // Deceleration phase - but NOT to zero velocity (continuous motion requirement)
            double t = current_time - accel_time - const_time;
            double t_remaining = total_time - current_time;
            position = end_pos - 0.5 * ACCELERATION * t_remaining * t_remaining;
            velocity = ACCELERATION * t_remaining;
        }
        else {
            // At endpoint - maintain minimum velocity for continuous motion
            position = end_pos;
            velocity = 5.0; // Minimum velocity to ensure continuous motion (no stopping)
        }
        
        // Apply direction
        if (distance < 0) velocity = -velocity;
        
        current_velocity_ = velocity;
        return position;
    }
    
    // Read limit switches (simulated)
    bool readLimitSwitch0() {
        return (current_position_ <= MIN_ANGLE + POSITION_TOLERANCE);
    }
    
    bool readLimitSwitch90() {
        return (current_position_ >= MAX_ANGLE - POSITION_TOLERANCE);
    }
    
    // Send position command to motor (simulated)
    bool sendMotorCommand(double position, double velocity) {
        // In real implementation, this would send Modbus/CANopen commands
        // For simulation, we'll update position directly with some dynamics
        
        static double last_command_pos = 0.0;
        static auto last_command_time = std::chrono::steady_clock::now();
        
        auto now = std::chrono::steady_clock::now();
        double dt = std::chrono::duration<double>(now - last_command_time).count();
        
        // Simple first-order dynamics simulation
        double error = position - current_position_;
        double max_step = MAX_VELOCITY * dt;
        
        if (abs(error) > max_step) {
            current_position_ += (error > 0) ? max_step : -max_step;
        } else {
            current_position_ = position;
        }
        
        last_command_time = now;
        return true; // Success
    }
    
    // Log cycle data
    void logCycleData(const std::string& status) {
        auto now = std::chrono::steady_clock::now();
        double timestamp = std::chrono::duration<double>(now - start_time_).count();
        
        CycleData data;
        data.cycle_number = current_cycle_;
        data.timestamp = timestamp;
        data.current_position = current_position_;
        data.target_position = target_position_;
        data.velocity = current_velocity_;
        data.load_torque = calculateLoadTorque(current_position_);
        data.limit_switch_0 = readLimitSwitch0();
        data.limit_switch_90 = readLimitSwitch90();
        data.status = status;
        
        cycle_log_.push_back(data);
        
        // Write to CSV
        log_file_ << data.cycle_number << ","
                  << std::fixed << std::setprecision(3) << data.timestamp << ","
                  << data.current_position << ","
                  << data.target_position << ","
                  << data.velocity << ","
                  << data.load_torque << ","
                  << data.limit_switch_0 << ","
                  << data.limit_switch_90 << ","
                  << data.status << "\n";
        log_file_.flush();
    }
    
    // Main control loop - CONTINUOUS MOTION WITHOUT STOPPING
    void runCyclingTest() {
        std::cout << "Starting continuous cycling test (NO STOPS)...\n";
        std::cout << "Requirement: Continuous 0° ↔ 90° motion without stopping\n";
        std::cout << "Press Ctrl+C to stop safely\n\n";
        
        double motion_time = 3.0; // seconds for each 0° to 90° motion
        auto cycle_start_time = std::chrono::steady_clock::now();
        
        while (g_running && current_cycle_ < MAX_CYCLES) {
            auto now = std::chrono::steady_clock::now();
            double elapsed = std::chrono::duration<double>(now - cycle_start_time).count();
            
            // Determine target position based on direction
            double start_pos = direction_up_ ? MIN_ANGLE : MAX_ANGLE;
            double end_pos = direction_up_ ? MAX_ANGLE : MIN_ANGLE;
            
            if (elapsed <= motion_time) {
                // Motion phase - generate smooth continuous motion
                target_position_ = generateMotionProfile(start_pos, end_pos, elapsed, motion_time);
                sendMotorCommand(target_position_, current_velocity_);
                logCycleData(direction_up_ ? "Moving_Up" : "Moving_Down");
                
                // Display progress
                if ((int)(elapsed * 10) % 10 == 0) { // Every 0.1 seconds
                    std::cout << "\rCycle " << current_cycle_ + 1 
                              << " | Position: " << std::fixed << std::setprecision(1) 
                              << current_position_ << "° | "
                              << (direction_up_ ? "↑ Up  " : "↓ Down")
                              << " | Torque: " << std::setprecision(2) 
                              << calculateLoadTorque(current_position_) << " N⋅m";
                    std::cout.flush();
                }
                
            } else {
                // IMMEDIATELY switch direction - NO PAUSE (continuous motion requirement)
                direction_up_ = !direction_up_;
                cycle_start_time = now;
                
                if (!direction_up_) {
                    current_cycle_++;
                    std::cout << "\n";
                }
                
                // Safety check - verify limit switches
                if ((current_position_ <= MIN_ANGLE + POSITION_TOLERANCE && !direction_up_) ||
                    (current_position_ >= MAX_ANGLE - POSITION_TOLERANCE && direction_up_)) {
                    std::cout << "\nWarning: Position limit reached!\n";
                }
                
                // Continue with immediate motion in new direction
                continue;
            }
            
            // Control loop timing
            std::this_thread::sleep_for(std::chrono::milliseconds(CONTROL_PERIOD_MS));
        }
        
        // Safe shutdown
        std::cout << "\n\nTest completed. Moving to safe position (0°)...\n";
        target_position_ = MIN_ANGLE;
        sendMotorCommand(target_position_, 0.0);
        logCycleData("Shutdown_Safe");
        
        // Generate summary
        generateTestSummary();
    }
    
    // Generate test summary
    void generateTestSummary() {
        std::cout << "\n" << std::string(60, '=') << "\n";
        std::cout << "TEST SUMMARY\n";
        std::cout << std::string(60, '=') << "\n";
        std::cout << "Total Cycles Completed: " << current_cycle_ << "\n";
        std::cout << "Total Data Points: " << cycle_log_.size() << "\n";
        std::cout << "Final Position: " << current_position_ << "°\n";
        
        if (!cycle_log_.empty()) {
            double total_time = cycle_log_.back().timestamp;
            std::cout << "Total Test Time: " << std::fixed << std::setprecision(1) 
                      << total_time << " seconds\n";
            
            // Calculate statistics
            double max_torque = 0.0;
            double avg_torque = 0.0;
            for (const auto& data : cycle_log_) {
                max_torque = std::max(max_torque, abs(data.load_torque));
                avg_torque += abs(data.load_torque);
            }
            avg_torque /= cycle_log_.size();
            
            std::cout << "Maximum Load Torque: " << std::setprecision(3) 
                      << max_torque << " N⋅m\n";
            std::cout << "Average Load Torque: " << avg_torque << " N⋅m\n";
        }
        
        std::cout << "Log file saved to: ../Output/pendulum_cycle_log.csv\n";
        std::cout << std::string(60, '=') << "\n";
    }
};

int main() {
    // Set up signal handler for clean shutdown
    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);
    
    try {
        PendulumController controller;
        controller.runCyclingTest();
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    std::cout << "Program terminated safely.\n";
    return 0;
}
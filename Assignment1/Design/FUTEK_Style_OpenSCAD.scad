// FUTEK-Style Horizontal Motor Test Bench
// Professional Configuration: Motor → Torque Sensor → Eddy Current Brake
// Based on Example 2 reference design

$fn = 50; // Smooth curves

// Design Parameters (matching FUTEK_Style_Parameters.py)
base_length = 1000.0;
base_width = 400.0;
base_height = 20.0;

motor_position_x = 150.0;
motor_mount_height = 100.0;
motor_stator_diameter = 85.0;
motor_stator_length = 44.4;
motor_shaft_extension = 50.0;

sensor_position_x = 500.0;
sensor_length = 100.0;
sensor_diameter = 50.0;
sensor_shaft_diameter = 25.0;

brake_position_x = 850.0;
brake_disc_diameter = 200.0;
brake_disc_thickness = 30.0;
brake_housing_width = 150.0;
brake_housing_height = 120.0;
brake_fin_count = 24;

main_shaft_diameter = 25.0;
main_shaft_length = 600.0;

pedestal_height = 100.0;
pedestal_width = 80.0;
pedestal_depth = 120.0;

// Colors (professional industrial scheme)
color_base = [0.7, 0.7, 0.7];       // Light gray (aluminum)
color_motor = [0.2, 0.3, 0.8];      // Blue (motor housing)
color_sensor = [0.8, 0.1, 0.1];     // Red (FUTEK branding)
color_brake = [0.3, 0.3, 0.3];      // Dark gray (cast iron)
color_shaft = [0.9, 0.9, 0.8];      // Light metallic (stainless)
color_pedestal = [0.8, 0.8, 0.9];   // Light blue (aluminum)
color_guard = [0.9, 0.9, 0.9, 0.7]; // Transparent (polycarbonate)

// Main assembly module
module futek_motor_test_bench() {
    // Base platform
    base_platform();
    
    // Motor assembly (left side)
    translate([motor_position_x, 0, 0])
        motor_assembly();
    
    // Torque sensor (center)
    translate([sensor_position_x, 0, motor_mount_height])
        torque_sensor_assembly();
    
    // Eddy current brake (right side)  
    translate([brake_position_x, 0, 0])
        brake_assembly();
    
    // Main shaft
    main_shaft_system();
    
    // Bearing pedestals
    bearing_pedestals();
    
    // Safety guards (optional - can be toggled)
    if (true) // Set to false to hide guards
        safety_guards();
}

module base_platform() {
    color(color_base)
    translate([0, -base_width/2, 0])
    difference() {
        // Main platform
        cube([base_length, base_width, base_height]);
        
        // Mounting holes (8 positions)
        for(i = [1:8]) {
            translate([i * base_length/9, base_width/2, -1])
                cylinder(d=8, h=base_height+2);
        }
        
        // Cable management slots
        translate([base_length/4, base_width/4, base_height/2])
            cube([20, base_width/2, base_height], center=true);
    }
}

module motor_assembly() {
    // Motor mount pedestal
    translate([0, 0, 0])
        bearing_pedestal();
    
    // Motor housing (simplified ILM-E85x30 representation)
    color(color_motor)
    translate([0, 0, motor_mount_height]) {
        rotate([0, 90, 0]) {
            // Stator housing
            cylinder(d=motor_stator_diameter, h=motor_stator_length);
            
            // Motor mounting flange
            translate([0, 0, -10])
                cylinder(d=motor_stator_diameter+20, h=10);
        }
        
        // Motor shaft extension
        translate([motor_stator_length, 0, 0])
            rotate([0, 90, 0])
                cylinder(d=main_shaft_diameter, h=motor_shaft_extension);
    }
}

module torque_sensor_assembly() {
    color(color_sensor) {
        // Sensor body (FUTEK TRS style)
        rotate([0, 90, 0]) {
            // Main sensor body
            cylinder(d=sensor_diameter, h=sensor_length);
            
            // Input shaft
            translate([0, 0, -20])
                cylinder(d=sensor_shaft_diameter, h=20);
            
            // Output shaft  
            translate([0, 0, sensor_length])
                cylinder(d=sensor_shaft_diameter, h=20);
            
            // Sensor label area
            translate([0, sensor_diameter/2-2, sensor_length/2])
                cube([sensor_diameter*0.8, 4, sensor_length*0.6], center=true);
        }
        
        // Mounting bracket
        translate([0, 0, -20])
            cube([sensor_length, 60, 20], center=true);
    }
}

module brake_assembly() {
    // Brake mount pedestal
    translate([0, 0, 0])
        bearing_pedestal();
    
    // Eddy current brake
    color(color_brake)
    translate([0, 0, motor_mount_height]) {
        // Brake housing
        translate([-brake_housing_width/2, -brake_housing_width/2, -20])
            cube([brake_housing_width, brake_housing_width, brake_housing_height]);
        
        // Brake disc with cooling fins
        rotate([0, 90, 0])
            brake_disc_with_fins();
    }
}

module brake_disc_with_fins() {
    // Main disc
    cylinder(d=brake_disc_diameter, h=brake_disc_thickness);
    
    // Cooling fins (radial pattern)
    for(i = [0:360/brake_fin_count:360-1]) {
        rotate([0, 0, i])
            translate([brake_disc_diameter/2-20, 0, brake_disc_thickness/2])
                cube([40, 3, brake_disc_thickness+10], center=true);
    }
    
    // Central hub
    cylinder(d=60, h=brake_disc_thickness+10);
}

module main_shaft_system() {
    color(color_shaft)
    translate([motor_position_x + motor_stator_length + motor_shaft_extension, 0, motor_mount_height])
        rotate([0, 90, 0])
            cylinder(d=main_shaft_diameter, 
                    h=brake_position_x - motor_position_x - motor_stator_length - motor_shaft_extension);
}

module bearing_pedestals() {
    // Motor-side pedestal
    translate([motor_position_x, 0, 0])
        bearing_pedestal();
    
    // Sensor-side pedestals (both sides of sensor)
    translate([sensor_position_x - 60, 0, 0])
        bearing_pedestal();
    translate([sensor_position_x + 60, 0, 0])
        bearing_pedestal();
    
    // Brake-side pedestal
    translate([brake_position_x, 0, 0])
        bearing_pedestal();
}

module bearing_pedestal() {
    color(color_pedestal) {
        // Pedestal base
        translate([-pedestal_width/2, -pedestal_depth/2, base_height])
            cube([pedestal_width, pedestal_depth, pedestal_height]);
        
        // Bearing housing (pillow block style)
        translate([0, 0, base_height + pedestal_height]) {
            difference() {
                // Housing block
                translate([-30, -40, 0])
                    cube([60, 80, 40]);
                
                // Bearing bore
                rotate([0, 90, 0])
                    cylinder(d=main_shaft_diameter+1, h=70, center=true);
            }
            
            // Housing cap
            translate([-25, -35, 35])
                cube([50, 70, 10]);
        }
    }
}

module safety_guards() {
    color(color_guard) {
        // Motor guard
        translate([motor_position_x, 0, motor_mount_height])
            rotate([0, 90, 0])
                cylinder(d=motor_stator_diameter+40, h=motor_stator_length+20);
        
        // Shaft guard (tunnel)
        translate([motor_position_x + 100, 0, motor_mount_height])
            rotate([0, 90, 0])
                difference() {
                    cylinder(d=80, h=400);
                    cylinder(d=60, h=410, center=true);
                }
        
        // Brake guard
        translate([brake_position_x, 0, motor_mount_height])
            rotate([0, 90, 0])
                cylinder(d=brake_disc_diameter+40, h=brake_disc_thickness+20);
    }
}

// Data acquisition components (simplified representation)
module daq_components() {
    // FUTEK USB interface
    color([0.2, 0.2, 0.2])
    translate([base_length/2, -base_width/2-50, base_height])
        cube([100, 30, 20]);
    
    // Handheld display
    color([0.1, 0.1, 0.1])
    translate([base_length/2+150, -base_width/2-50, base_height])
        cube([80, 40, 15]);
    
    // Connection cables (simplified)
    color([1, 1, 0]) // Yellow cables
    translate([sensor_position_x, base_width/2, motor_mount_height+20])
        rotate([45, 0, 0])
            cylinder(d=10, h=100);
}

// Assembly labels (for identification)
module assembly_labels() {
    // Title
    translate([base_length/2, -base_width/2-100, 0])
        color([0, 0, 0])
            text("FUTEK-Style Motor Test Bench", 
                 size=16, halign="center", font="Arial:style=Bold");
    
    // Component labels
    translate([motor_position_x, -base_width/2-50, 0])
        color([0, 0, 0])
            text("ILM-E85x30 Motor", size=10, halign="center");
    
    translate([sensor_position_x, -base_width/2-50, 0])
        color([0, 0, 0])
            text("FUTEK TRS Sensor", size=10, halign="center");
    
    translate([brake_position_x, -base_width/2-50, 0])
        color([0, 0, 0])
            text("Eddy Current Brake", size=10, halign="center");
}

// Main assembly call
futek_motor_test_bench();

// Optional components (uncomment to include)
daq_components();
// assembly_labels();  // Uncomment for labels
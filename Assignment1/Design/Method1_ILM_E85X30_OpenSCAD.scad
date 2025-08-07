// Method 1: Reaction Torque Cradle for ILM-E85X30 Motor
// OpenSCAD parametric design for cradle mount torque testing

$fn = 50; // Smooth curves

// Design Parameters based on ILM-E85X30 specifications
base_length = 800;
base_width = 600;
base_height = 40;

motor_stator_diameter = 85;
motor_stator_length = 44.4;
motor_rotor_bore = 52;
motor_mount_height = 150;

cradle_arm_length = 400;
pedestal_height = 120;
pedestal_width = 100;
pedestal_depth = 80;

torque_arm_length = 300;
torque_arm_width = 30;
torque_arm_thickness = 10;

// Colors for different components
color_base = [0.5, 0.5, 0.5];          // Gray (cast iron base)
color_motor = [0.2, 0.3, 0.8];         // Blue (motor)
color_cradle = [0.8, 0.8, 0.9];        // Light blue (aluminum cradle)
color_torque_arm = [0.9, 0.7, 0.1];    // Yellow (steel torque arm)
color_load_cell = [0.8, 0.1, 0.1];     // Red (load cell)
color_bearings = [0.7, 0.7, 0.8];      // Steel gray (bearings)

// Main assembly
module method1_cradle_assembly() {
    // Base platform
    base_platform();
    
    // Motor (ILM-E85X30)
    translate([0, 0, motor_mount_height])
        rotate([90, 0, 0])
            ilm_e85x30_motor();
    
    // Cradle pedestals with trunnion bearings
    cradle_pedestals();
    
    // Torque measurement system
    torque_measurement_system();
    
    // Safety features
    safety_guards();
}

module base_platform() {
    color(color_base) {
        difference() {
            // Main base
            translate([-base_length/2, -base_width/2, 0])
                cube([base_length, base_width, base_height]);
            
            // Mounting holes for floor anchoring
            for(x = [-300, 0, 300]) {
                for(y = [-200, 0, 200]) {
                    translate([x, y, -1])
                        cylinder(d=16, h=base_height+2);
                }
            }
        }
        
        // Reinforcement ribs for reaction forces
        for(i = [0:4]) {
            translate([-base_length/2 + 100 + i*120, -base_width/2 + 50, base_height-10])
                cube([base_width-100, 20, 10]);
        }
    }
}

module ilm_e85x30_motor() {
    color(color_motor) {
        difference() {
            // Motor stator (outer cylinder)
            cylinder(d=motor_stator_diameter, h=motor_stator_length);
            
            // Motor rotor bore (inner cylinder)  
            translate([0, 0, -1])
                cylinder(d=motor_rotor_bore, h=motor_stator_length+2);
        }
        
        // Motor mounting features
        translate([0, 0, -5])
            cylinder(d=motor_stator_diameter+10, h=5);
    }
    
    // Rotor shaft (simplified)
    color(color_bearings)
    translate([0, 0, -20])
        cylinder(d=25, h=motor_stator_length+40);
}

module cradle_pedestals() {
    // Left pedestal
    color(color_cradle) {
        translate([-cradle_arm_length/2 - pedestal_width/2, -pedestal_depth/2, base_height])
            difference() {
                cube([pedestal_width, pedestal_depth, pedestal_height]);
                
                // Trunnion bearing bore
                translate([pedestal_width/2, pedestal_depth/2, pedestal_height/2])
                    rotate([0, 90, 0])
                        cylinder(d=25, h=pedestal_width+2, center=true);
            }
    }
    
    // Right pedestal (mirror of left)
    color(color_cradle) {
        translate([cradle_arm_length/2 - pedestal_width/2, -pedestal_depth/2, base_height])
            difference() {
                cube([pedestal_width, pedestal_depth, pedestal_height]);
                
                // Trunnion bearing bore
                translate([pedestal_width/2, pedestal_depth/2, pedestal_height/2])
                    rotate([0, 90, 0])
                        cylinder(d=25, h=pedestal_width+2, center=true);
            }
    }
    
    // Trunnion bearings
    color(color_bearings) {
        // Left bearing
        translate([-cradle_arm_length/2, 0, base_height + pedestal_height/2])
            rotate([0, 90, 0])
                difference() {
                    cylinder(d=60, h=20, center=true);
                    cylinder(d=25, h=25, center=true);
                }
        
        // Right bearing
        translate([cradle_arm_length/2, 0, base_height + pedestal_height/2])
            rotate([0, 90, 0])
                difference() {
                    cylinder(d=60, h=20, center=true);
                    cylinder(d=25, h=25, center=true);
                }
    }
    
    // Cradle connecting arm
    color(color_cradle)
    translate([-cradle_arm_length/2, -30, base_height + pedestal_height/2 - 20])
        cube([cradle_arm_length, 60, 40]);
}

module torque_measurement_system() {
    // Main torque arm
    color(color_torque_arm) {
        translate([0, -torque_arm_width/2, motor_mount_height + motor_stator_diameter/2 + 20])
            cube([torque_arm_length, torque_arm_width, torque_arm_thickness]);
        
        // Connection to motor housing
        translate([0, 0, motor_mount_height + motor_stator_diameter/2 + 10])
            cylinder(d=30, h=torque_arm_thickness + 20);
    }
    
    // Load cell at end of torque arm
    color(color_load_cell) {
        translate([torque_arm_length/2, 0, motor_mount_height + motor_stator_diameter/2 + 30])
            cylinder(d=25, h=50);
        
        // Load cell mounting bracket
        translate([torque_arm_length/2 - 30, -20, motor_mount_height + motor_stator_diameter/2 + 80])
            cube([60, 40, 20]);
    }
    
    // Force measurement indicator (visualization)
    color([1, 1, 0]) // Yellow arrow
    translate([torque_arm_length/2, 0, motor_mount_height + motor_stator_diameter/2 + 100])
        cylinder(d=5, h=30);
}

module safety_guards() {
    // Motor safety guard (transparent)
    color([0.9, 0.9, 0.9, 0.3]) {
        translate([0, 0, motor_mount_height])
            rotate([90, 0, 0])
                difference() {
                    cylinder(d=motor_stator_diameter+50, h=motor_stator_length+20, center=true);
                    cylinder(d=motor_stator_diameter+45, h=motor_stator_length+25, center=true);
                    
                    // Opening for torque arm
                    translate([-50, -(torque_arm_width+10)/2, -motor_stator_length/2-15])
                        cube([100, torque_arm_width+10, motor_stator_length+30]);
                }
    }
    
    // Emergency stop button (simplified representation)
    color([1, 0, 0]) // Red
    translate([-200, -200, 200])
        cylinder(d=50, h=20);
}

// Information panel (text annotations)
module info_panel() {
    translate([base_length/2 + 50, -base_width/2, 0]) {
        color([0, 0, 0])
        text("METHOD 1: REACTION TORQUE CRADLE", size=10);
        
        translate([0, -30, 0])
        color([0, 0, 0])
        text("Motor: ILM-E85X30 (85mm frameless)", size=8);
        
        translate([0, -50, 0])
        color([0, 0, 0])
        text("Measurement: Load Cell × 300mm Arm", size=8);
        
        translate([0, -70, 0])
        color([0, 0, 0])
        text("Max Torque: 15 Nm", size=8);
        
        translate([0, -90, 0])
        color([0, 0, 0])
        text("Accuracy: ±1% typical", size=8);
    }
}

// Assembly labels for major components
module component_labels() {
    // Base label
    translate([0, -base_width/2 - 30, 0])
        color([0, 0, 0])
            text("REINFORCED BASE PLATFORM", size=8, halign="center");
    
    // Motor label
    translate([0, motor_stator_diameter/2 + 40, motor_mount_height])
        color([0, 0, 0])
            text("ILM-E85X30 MOTOR", size=8, halign="center");
    
    // Torque arm label
    translate([torque_arm_length/4, torque_arm_width/2 + 10, motor_mount_height + motor_stator_diameter/2 + 35])
        color([0, 0, 0])
            text("TORQUE ARM (300mm)", size=6, halign="center");
    
    // Load cell label
    translate([torque_arm_length/2, 30, motor_mount_height + motor_stator_diameter/2 + 60])
        color([0, 0, 0])
            text("LOAD CELL", size=6, halign="center");
}

// Main assembly with options
method1_cradle_assembly();
info_panel();

// Uncomment for component labels
// component_labels();

// Design summary
echo("METHOD 1 DESIGN SUMMARY:");
echo(str("Base Platform: ", base_length, "×", base_width, "×", base_height, "mm"));
echo(str("Motor: ILM-E85X30 (", motor_stator_diameter, "mm stator)"));
echo(str("Torque Arm: ", torque_arm_length, "mm length"));
echo(str("Cradle Span: ", cradle_arm_length, "mm between pedestals"));
echo("Measurement Principle: Reaction Torque = Force × Arm Length");
echo(str("Expected Accuracy: ±1% (", torque_arm_length, "mm arm length)"));
// OpenSCAD Model: ILM-E85x30 Motor Test Bed
// Generated from Assignment 1 parametric design
// Usage: Open in OpenSCAD and render

$fn = 50; // Smooth curves

// Design Parameters
base_length = 800.0;
base_width = 600.0;
base_height = 150.0;

housing_outer_dia = 150.0;
housing_length = 80.0;
housing_bore_dia = 85.0;

shaft_diameter = 50.0;
shaft_length = 400.0;

// Colors
color_base = [0.5, 0.5, 0.5];      // Gray (Cast Iron)
color_housing = [0.8, 0.8, 0.9];   // Light Blue (Aluminum)
color_shaft = [0.9, 0.9, 0.7];     // Light Yellow (Steel)
color_mount = [0.7, 0.7, 0.9];     // Light Purple

module base_frame() {
    color(color_base)
    translate([-base_length/2, -base_width/2, 0])
    cube([base_length, base_width, base_height]);
}

module motor_housing() {
    color(color_housing)
    translate([0, 0, base_height])
    difference() {
        cylinder(d=housing_outer_dia, h=housing_length);
        translate([0, 0, -1])
        cylinder(d=housing_bore_dia, h=housing_length+2);
    }
}

module main_shaft() {
    color(color_shaft)
    translate([0, 0, base_height - shaft_length/4])
    cylinder(d=shaft_diameter, h=shaft_length);
}

module sensor_mount() {
    color(color_mount)
    translate([50, -75, base_height])
    cube([200, 150, 25]);
}

module cooling_fins() {
    color(color_housing)
    translate([0, 0, base_height])
    for(i = [0:30:330]) {
        rotate([0, 0, i])
        translate([housing_outer_dia/2, -2.5, 0])
        cube([15, 5, housing_length]);
    }
}

// Assembly
module motor_test_bed() {
    base_frame();
    motor_housing();
    cooling_fins();
    main_shaft();
    sensor_mount();
}

// Generate the complete assembly
motor_test_bed();

// Add text labels
translate([0, -base_width/2 - 50, 0])
color([0, 0, 0])
text("ILM-E85x30 Motor Test Bed", size=20, halign="center");

translate([0, -base_width/2 - 80, 0])
color([0, 0, 0])
text("Assignment 1 - Parametric Design", size=12, halign="center");

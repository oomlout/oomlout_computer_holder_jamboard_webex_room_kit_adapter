$fn = 50;


difference() {
	union() {
		hull() {
			translate(v = [-24.5000000000, 39.5000000000, 0]) {
				cylinder(h = 3, r = 5);
			}
			translate(v = [24.5000000000, 39.5000000000, 0]) {
				cylinder(h = 3, r = 5);
			}
			translate(v = [-24.5000000000, -39.5000000000, 0]) {
				cylinder(h = 3, r = 5);
			}
			translate(v = [24.5000000000, -39.5000000000, 0]) {
				cylinder(h = 3, r = 5);
			}
		}
	}
	union() {
		#translate(v = [7.5000000000, 7.5000000000, 0.0000000000]) {
			cylinder(h = 3, r = 15);
		}
		#translate(v = [-7.5000000000, -82.5000000000, 0]) {
			cube(size = [30, 90, 3]);
		}
		#translate(v = [-34.6000000000, -78.5000000000, 0]) {
			rotate(a = [0, 0, 342.5000000000]) {
				cube(size = [30, 90, 3]);
			}
		}
		#translate(v = [-66.0000000000, 32.5000000000, 0]) {
			cube(size = [100, 85, 3]);
		}
		#translate(v = [18.7500000000, 25.0000000000, 0]) {
			cube(size = [7.5000000000, 100, 3]);
		}
	}
}
void fac(n) {
	int f = 1;
	while (n > 1) {
		f = f * n;
		n = n - 1;
	}
}

void main() {
	fac(5);
}
void fib(n) {
    int n1 = 1;
    int n2 = 1;
    int n3 = 1;
    int count = n - 2;
    while (count) {
        n3 = n1 + n2;
        n1 = n2;
        n2 = n3;
        count = count - 1;
    }
}

void printf(mes) {
    stdout = stdout + mes;
}

void main() {
    fib(10);
    printf("'fibonacci of 10: '+str(n2)");
}

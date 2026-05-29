class BankAccount { String accountNumber; double balance; BankAccount(String accNo, double
bal) { accountNumber = accNo; balance = bal; } void deposit(double amount) { balance += amount;
} void withdraw(double amount) { if (balance >= amount) { balance -= amount; } else {
System.out.println("Insufficient funds"); } } void display() { System.out.println("Account Number: " +
accountNumber); System.out.println("Balance: " + balance); } } class SavingsAccount extends
BankAccount { double interestRate; SavingsAccount(String accNo, double bal, double rate) {
super(accNo, bal); interestRate = rate; } void addInterest() { balance += balance * interestRate /
100; } void display() { super.display(); System.out.println("Interest Rate: " + interestRate + "%"); } }
class CheckingAccount extends BankAccount { double overdraftLimit; CheckingAccount(String
accNo, double bal, double limit) { super(accNo, bal); overdraftLimit = limit; } void withdraw(double
amount) { if (balance - amount >= -overdraftLimit) { balance -= amount; } else {
System.out.println("Withdrawal exceeds overdraft limit"); } } void display() { super.display();
System.out.println("Overdraft Limit: " + overdraftLimit); } } class BankTest { public static void
main(String args[]) { SavingsAccount sa = new SavingsAccount("SA101", 5000, 5.0);
CheckingAccount ca = new CheckingAccount("CA201", 2000, 1000); sa.deposit(1000);
ca.deposit(500); ca.withdraw(2500); ca.withdraw(2000); sa.addInterest(); System.out.println("---Savings Account Details ---"); sa.display(); System.out.println("--- Checking Account Details ---");
ca.display(); } }
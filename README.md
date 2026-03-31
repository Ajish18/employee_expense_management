### Etems

 

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app etems
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/etems
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
# employee_expense_management



ETEMS - Employee Travel and Expense MAnagement System

Workflow:

Travel Request:
The employee first creates the Travel Request, before their Travel and can claim the advance amount.

The Employee Creates a Travel Request -> It will be first approved or rejected by their repective reporting manager -> the finance manager then approve/reject if approved advance is given else not.

Expense Claim:
The employee after Travel creates the expense claims, the amount they spent on what and also include their travel request. Employee fills all the required details and click submit action.

The Reporting manager verifies it and approve/reject it.

If approved the status will be in Pending Finance verification, the finance user verifies it, whether the bill are submitted or not he checks itand enter the approved amount. And clicks verified.
The advance amount along with the ampproved amount are calculated and the balance payable and balance receivable are set.
The finance user has the right to reject the expense claim too.

If verified, the status will be in verified and the finance manager will finally settle or receive the amount, the payment transaction will be done in Expense payable or Expense Receivable doctype. Once the amount is settled completely, it will be state becomes settled.
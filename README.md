# FinTech Credit Risk Prediction


## Content 

* notebooks : 
    - logistic_regression.ipynb `Logistic Regression`
    - bagging.ipynb `Bagging (Random Forest)`
    - boosting.ipynb `boosting using xgboost algorithm`

**We use bagging**

## JSON example

```
{
  "person_age": 22,
  "person_income": 59000,
  "person_home_ownership": "RENT",
  "person_emp_length": 123.0,
  "loan_intent": "PERSONAL",
  "loan_grade": "D",
  "loan_amnt": 35000,
  "loan_int_rate": 16.02,
  "loan_status": 1,
  "loan_percent_income": 0.59,
  "cb_person_default_on_file": "Y",
  "cb_person_cred_hist_length": 3
}
```

## Objective

to predict risk, the target variable in your dataset would typically be:

 `loan_status`
 
This variable indicates whether the loan was successful (e.g., paid back) or not (e.g., defaulted). In your dataset:

- **1** means the loan was approved or successful.

- **0** (if present in other rows) would represent a failed or defaulted loan.
By predicting the loan_status, you can determine whether a borrower is likely to default (high risk) or successfully repay the loan (low risk).


## Explanation 

1. **person_age:**

Represents the age of the individual applying for the loan. In this case, the person is 22 years old.

2. **person_income:**

The annual income of the individual in monetary terms. Here, it is $59,000.

3. **person_home_ownership:**

Indicates the homeownership status of the person. Possible values could be "RENT," "OWN," "MORTGAGE," etc. In this example, the person rents their home.

4. **person_emp_length:**

The length of time (in months) the individual has been employed. Here, it is 123 months (approximately 10 years and 3 months).

5. **loan_intent:**

The purpose or intent of the loan. Examples might include "PERSONAL," "EDUCATION," "MEDICAL," "DEBTCONSOLIDATION," etc. In this case, the loan is for personal use.

6. **loan_grade:**

A risk assessment grade assigned to the loan, typically based on the creditworthiness of the borrower. Grades may range from "A" (best) to "G" (highest risk). Here, the loan grade is "D."

7. **loan_amnt:**

The amount of the loan requested by the borrower. In this case, it is $35,000.

8. **loan_int_rate:**

The interest rate applied to the loan as a percentage. Here, it is 16.02%.

9.** loan_status:**

Indicates whether the loan was approved (1) or not (0). In this case, the loan was approved.

10. **loan_percent_income:**

Represents the ratio of the loan amount to the person's income, expressed as a percentage. This value is used to assess affordability. Here, it is 0.59, meaning 59% of the person's annual income is equivalent to the loan amount.

11. **cb_person_default_on_file:**

Indicates whether the individual has a history of defaulting on loans. "Y" means yes, the person has a history of default, while "N" means no. Here, the individual has a history of default ("Y").

12. **cb_person_cred_hist_length:**

The length of the person's credit history in years. Here, it is 3 years.

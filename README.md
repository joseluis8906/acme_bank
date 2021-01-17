# acme_bank
not available

## dependencies to run in a local environment
1. python3
2. pipenv https://pypi.org/project/pipenv/
3. make https://www.gnu.org/software/make/
4. docker https://docs.docker.com/engine/install/
5. docker-compose https://docs.docker.com/compose/install/

## to run the tests
make test

### to run the project
make run

### to clean the project (remove docker containers, networks, etc)
make clean

## usage
the project consists of three endpoints:

- status
```
curl --location --request GET 'localhost:8080/status'
```

- accounts:
```
curl --location --request PUT 'localhost:8080/accounts' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": "105398891",
    "pin": "2090",
    "balance": "500000"
}'
```

- transactions:
```
curl --location --request POST 'localhost:8080/transaction' \
--form 'data=@/Users/jhon_doe/Development/acme_bank/assets/obj.json'
```

after running the project, you should verify that the `status` endpoint responds with: 
```
{
    "data": "up and running",
    "error": null
}
```

after that you must create an account with the enpoint /accounts and with the body below to which the transaction will be made:
```
{
    "data": {
        "balance": "500000",
        "pin": "2090",
        "user_id": "105398891"
    },
    "error": null
}
```

as a last step you must verify your json file that contains the transactions that will be applied to the newly created account, things to check before submitting
the request:
1. the user_id and pin is the same as the account, if they are different you will be receive a validation error
2. if while the transactions are carried out the account runs out of balance, you will be receive a balance error
3. if one of the actions in the json file doesn't exists in the transactions, you will be receive a invalid action error

at any time you can update or restart the registered account through the /accounts endpoint, the update is done based on the user_id property.

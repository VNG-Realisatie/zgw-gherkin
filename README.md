# ZGW-Gherkin

## Table of Contents

- [How to Add tests](#how-to-add-tests)
  - [Before You Begin](#before-you-begin)
  - [Project Structure](#structure)
  - [Example](#example)
  - [Adding Tags](#adding-tags)
- [How to Run](#how-to-run)
  - [Run Locally](#run-locally)
  - [Run on Docker](#run-on-docker)

# How to Add tests

## Before you begin

Basic usages can be found here:

https://behave.readthedocs.io/en/latest/

## Structure

The basic structure for every gherkin project is the following:

```
|-- environment.py
|-- features
|   |-- example.feature
|-- steps
|   |-- example.py
|-- flows
|   |-- flow.py
```

`flows` is the only one that is specific to this project.

## Example

Let's say you want to add a gherkin test:

```gherkin
#language: nl

Functionaliteit: Catalogi items moeten aan bepaalde regels voldoen
  Om te testen dat een catalogi items aan te maken zijn
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen en waar nodig aanvullen
  Zodat ik de catalogus als basis kan gebruiken voor verdere acties

Scenario: aanmaken van een catalogus
  Gegeven de catalogus-api is beschikbaar
  Als er een nieuwe valide catalogus aangemaakt wordt
  Dan krijgt de gebruiker statuscode 201 terug
```

You would add a feature file to `features`, let's call it `example.feature`

Depending on your IDE running this feature file would already create steps (pycharm understands behave for example).

But you would need to add these steps to `steps` let's call that file `example.py`

```python
from behave import *

@step("de catalogus-api is beschikbaar")
def step_impl(context):
    response = context.client.catalogus.check_available()
    assert response.status_code == 200
    return

@step("er een nieuwe valide catalogus aangemaakt wordt")
def step_impl(context):
    context.flow.setup_catalogus()
    context.response = context.flow.catalogus
    return


@step("krijgt de gebruiker statuscode {status_code:d} terug")
def step_impl(context, status_code):
    response = context.response
    assert response.status_code == status_code
```

Now if you look at the actual code you would see that the last `THEN` is part of `generic.py` that is because this step is shared across most tests.
It makes sense to assert at some point that the correct `status_code` is returned so having that `step` is a shareable step makes sense.

Now most if not all `steps` use the `context.flow` this houses all logic related to creating/updating/deleting and keeping track of items created during tests.
The `flow` uses the `client/*` (`from client import endpoints, zgw`) to make the actual calls. Where each specific action for a specific api is housed.

Feel free to change this system. At time of this writing the number of features and calls was manageable but it might well get out of hand and become a mess.

## Adding Tags

Tags are a specific way that behave interacts with tests. Here they are used to created certain fixtures. 

See the docs: https://behave.readthedocs.io/en/latest/tutorial/#controlling-things-with-tags

Example:

```gherkin
#language: nl

Functionaliteit: Catalogi items moeten aan bepaalde regels voldoen
  Om te testen dat een catalogi items aan te maken zijn
  Als een gebruiker van het ZGW
  Wil ik het systeem kunnen bevragen en waar nodig aanvullen
  Zodat ik de catalogus als basis kan gebruiken voor verdere acties
  
@token.set
@catalogus
Scenario: een aangemaakt catalogus is via filters terug te vinden
  Gegeven de catalogus-api is beschikbaar
  Als de catalogus wordt gezocht met parameters
  | parameter |
  | rsin      |
  | domein    |
  Dan krijgt de gebruiker de catalogus terug met de juiste informatie
```

The `Scenario` has two tags. One which sets a token and one that creates a catalogus before the test. 
This way scenario's can be kept clean, you do not need a `given` step that says: "create a token and set that token and create a catalogus".

How are these tags handled? In `environment.py` there is a function:

```python
def before_tag(context, tag):
    print(f"working on tag: {tag}")
    match tag:
        case "catalogus":
            use_fixture(setup_flow, context)
            context.flow.setup_catalogus()
        case "token.set":
            set_token(context)
        case "zaak.basis":
            use_fixture(setup_flow, context)
            context.flow.prerequisites_zaak()
        case "zaak.compleet":
            use_fixture(setup_flow, context)
            context.flow.complete_zaak()
        case _:
            print(f"unknown tag: {tag}")

    return
```

This will match a tag and then runs that as part of either the flow (so you have the catalogus_id within that Object for example) or as a different function (such as setting the token).

If you create a new tag be sure that add it to the `allow_list` within `envoriment.py`:

```python
VALID_TAGS = ["archiveren.valide", "catalogus", "zaak.basis", "zaak.compleet"]
```

# How to run

## Run locally

1. Create a venv and activate
2. Install packages
```shell
pip install -r requirements.txt
```
3. Run behave
```shell
behave
```

## Run on docker

1. Build image (change the tag as needed)
```shell
docker build -t systeem-tests:v0.1 .
```
2. Run a container
```shell
docker run --name test -d -e TOKEN=${YOUR_TOKEN} systeem-tests:v0.1
```
3. Retrieve logs
```shell
docker logs test
```

Alternativly you can run command 2 without the `-d` flag.

from aiogram.dispatcher.filters.state import State, StatesGroup

class FormStates(StatesGroup):
    full_name_input = State()
    date_of_birth_input = State()
    phone_input = State()
    phone_tied = State()
    username_input = State()
    city_input = State()
    transport_input = State()
    qr_code_input = State()
    submit_form = State()


class RegisterStates(StatesGroup):
    full_name_input = State()
    phone_input = State()
    city_input = State()


class TrackStates(StatesGroup):
    code_input = State()
    items_upload = State()
    delete_input = State()


class RansomStates(StatesGroup):
    code_input = State()
    items_upload = State()
    delete_input = State()
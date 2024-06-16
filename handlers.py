from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
import utils

router = Router()  # Создаем экземпляр Router
class main_states(StatesGroup):
    #Шаги состояний
    tech = State()
    tvorch= State()
    it = State()
    econom = State()
    result = State()


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer("Привет, я профориентационный бот Физтех-колледжа. Я задам тебе вопросы после ответа на которые, я расскажу тебе о твоей предрассположенности к разным видам деятельности", reply_markup=kb.start_kb)

@router.message(F.text.lower() == "начать тестирование")
@router.message(Command("начать тестирование"))
async def menu_cmd(message: types.Message, state=FSMContext):
    await message.answer("я называю действие, а ты посредством кнопок или словами Да/Нет отвечаешь, интересно ли оно тебе и хотел/a ли бы ты этому научиться")
    await state.set_state(main_states.tech)
    await message.answer(config.questions_tech[0],reply_markup=kb.started_kb)
    await state.update_data(tech2=0)
    await state.update_data(tech1=0)
    await state.update_data(current_question_tech=1)
    

@router.message(main_states.tech, F.text.lower().in_({"да","нет","да👍","нет👎"}))
async def techprocces(message: Message, state=FSMContext):
    tech =  await state.get_data()
    
    if tech["tech2"] < 4 and tech["current_question_tech"] < len(config.questions_tech):
        if "да" in message.text.lower():
            tech["tech1"] +=1
            await state.update_data(tech1=tech["tech1"])
        elif "нет" in message.text.lower() :
            tech["tech2"] +=1
            await state.update_data(tech2=tech["tech2"])
        await message.answer(config.questions_tech[tech["current_question_tech"]],reply_markup=kb.started_kb)
        tech["current_question_tech"] += 1
        await state.update_data(current_question_tech=tech["current_question_tech"])  
        
    else:
        await state.set_state(main_states.tvorch)
        await message.answer(config.questions_tvorch[0])
        await state.update_data(tvorch1=0)
        await state.update_data(tvorch2=0)
        await state.update_data(current_question_tvorch=1)


@router.message(main_states.tvorch, F.text.lower().in_({"да","нет","да👍","нет👎"}))   
async def tvorchprocces(message: Message, state=FSMContext):
    tvorch =  await state.get_data()
    
    if tvorch["tvorch2"] < 4 and tvorch["current_question_tvorch"] < len(config.questions_tvorch):
        if "да" in message.text.lower():
            tvorch["tvorch1"] +=1
            await state.update_data(tvorch1=tvorch["tvorch1"])
        elif "нет" in message.text.lower():
            tvorch["tvorch2"] +=1
            await state.update_data(tvorch2=tvorch["tvorch2"])
        await message.answer(config.questions_tvorch[tvorch["current_question_tvorch"]],reply_markup=kb.started_kb)
        tvorch["current_question_tvorch"] += 1
        
        await state.update_data(current_question_tvorch=tvorch["current_question_tvorch"])      
        
    else:
        await state.set_state(main_states.it)
        await state.update_data(it1=0)
        await state.update_data(it2=0)
        await message.answer(config.questions_it[0])
        await state.update_data(current_question_it=1)
        

@router.message(main_states.it, F.text.lower().in_({"да","нет","да👍","нет👎"}))
async def itprocces(message: Message, state=FSMContext):
    it =  await state.get_data()
    
    if it["it2"] < 4 and it["current_question_it"] < len(config.questions_it):
        if "да" in message.text.lower():
            it["it1"] +=1
            await state.update_data(it1=it["it1"])
        elif "нет" in message.text.lower() :
            it["it2"] +=1
            await state.update_data(it2=it["it2"])
        await message.answer(config.questions_it[it["current_question_it"]], reply_markup=kb.started_kb)
        it["current_question_it"] += 1
        await state.update_data(current_question_it=it["current_question_it"])      
    else:
        await state.set_state(main_states.econom)
        await state.update_data(econom1=0)
        await state.update_data(econom2=0)
        await message.answer(config.questions_econom[0])
        await state.update_data(current_question_econom=1)

@router.message(main_states.econom, F.text.lower().in_({"да","нет","да👍","нет👎"}))
async def economprocces(message: Message, state=FSMContext):
    econom =  await state.get_data()
    print(econom["current_question_econom"])

    if econom["econom2"] < 4 and econom["current_question_econom"] < len(config.questions_econom):
        if "да" in message.text.lower():
            econom["econom1"] +=1
            
            await state.update_data(econom1=econom["econom1"])
        elif "нет" in message.text.lower():
            econom["econom2"] +=1
            await state.update_data(econom2=econom["econom2"])
        await message.answer(config.questions_econom[econom["current_question_econom"]], reply_markup=kb.started_kb)
        econom["current_question_econom"] += 1
        await state.update_data(current_question_econom=econom["current_question_econom"])      
        
    else:
        await state.set_state(main_states.result)
        

@router.message(main_states.result)
async def user_result(message: Message, state=FSMContext):
    data = await state.get_data()
    result = {}
    keys_to_extract= ["it1","tvorch1","tech1","econom1"]
    for key in keys_to_extract:
        if key in data:
            result[key] = data[key]
    print(result)
    maxvalue = float('-inf')
    maxkey = None
    for key, value in result.items():
        if value > maxvalue:
            maxvalue = value #максимальное значение всех веток 
            maxkey = key #ключ ветки максимального значения
            
    if maxvalue < 5:
        await utils.undefined(message)
    else:
        if maxkey == "it1":
            await  utils.it_end(message)
        elif maxkey == "tech1":
            await utils.tech_end(message)
        elif maxkey == "tvorch1":
            await utils.tvorch_end(message)
        elif maxkey == "econom1":
            await utils.econom_end(message)
    await state.clear()

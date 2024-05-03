from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import kb

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
import utils

router = Router()  # управляет всеми процессами в файле
class main_states(StatesGroup):
    #Шаги состояний
    tech = State()
    tvorch= State()
    it = State()
    econom = State()
    result = State()

#обрабатыевает команду старт
@router.message(Command('start')) 
async def start_handler(msg: Message):
    await msg.answer("Привет ✌️, я профориентационный бот Физтех-колледжа. Я задам тебе вопросы после ответа на которые, я расскажу тебе о твоей предрассположенности к разным видам деятельности", reply_markup=kb.start_kb)
#запускает тест. ставит 1 стейт и обозначает переменные счетчики. срабатывает в случае соотвествующей команды
@router.message(F.text.lower() == "начать тестирование")
@router.message(Command("начать тестирование"))
async def menu_cmd(message: types.Message, state=FSMContext):
    await message.answer("я называю действие, а ты посредством кнопок или словами Да/Нет отвечаешь, интересно ли оно тебе и хотел/a ли бы ты этому научиться")
    await state.set_state(main_states.tech)
    await message.answer(config.questions_tech[0],reply_markup=kb.started_kb)     #отправляет 1 вопрос для сработки хендлера
    await state.update_data(tech2=0)
    await state.update_data(tech1=0) #подготавливает для хранения данных
    await state.update_data(current_question_tech=1)
    
#основной процесс теста, получает ответы да/нет и на основании этого в сохраняет количество ответов в переменные-счетчики
@router.message(main_states.tech, F.text.lower().in_({"да","нет"}))
async def techprocces(message: Message, state=FSMContext):
    tech =  await state.get_data()
    
    if tech["tech2"] < 4 and tech["current_question_tech"] < len(config.questions_tech): #проверяет по состоянию, на количество ответов "нет" и кол-ву заданных вопросов
        if message.text.lower() == "да":
            tech["tech1"] +=1   #добавляет +1 в счетчек ответов да, если ответ "да"
            await state.update_data(tech1=tech["tech1"])
        elif message.text.lower() == "нет":
            tech["tech2"] +=1 #добавляет +1 в счетчек ответов нет, если ответ "нет"
            await state.update_data(tech2=tech["tech2"])
        await message.answer(config.questions_tech[tech["current_question_tech"]],reply_markup=kb.started_kb)  #задает вопрос из конфиг файла
        tech["current_question_tech"] += 1
        await state.update_data(current_question_tech=tech["current_question_tech"])  
        
    else:
        await state.set_state(main_states.tvorch)
        await message.answer(config.questions_tvorch[0])
        await state.update_data(tvorch1=0)
        await state.update_data(tvorch2=0)
        await state.update_data(current_question_tvorch=1)

#основной процесс теста, получает ответы да/нет и на основании этого в сохраняет количество ответов в переменные-счетчики
@router.message(main_states.tvorch, F.text.lower().in_({"да","нет"}))
async def tvorchprocces(message: Message, state=FSMContext):
    tvorch =  await state.get_data()
    
    if tvorch["tvorch2"] < 4 and tvorch["current_question_tvorch"] < len(config.questions_tvorch):
        if message.text.lower() == "да":
            tvorch["tvorch1"] +=1
            await state.update_data(tvorch1=tvorch["tvorch1"])
        elif message.text.lower() == "нет":
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
        
#основной процесс теста, получает ответы да/нет и на основании этого в сохраняет количество ответов в переменные-счетчики
@router.message(main_states.it, F.text.lower().in_({"да","нет"}))
async def itprocces(message: Message, state=FSMContext):
    it =  await state.get_data()
    
    if it["it2"] < 4 and it["current_question_it"] < len(config.questions_it):
        if message.text.lower() == "да":
            it["it1"] +=1
            await state.update_data(it1=it["it1"])
        elif message.text.lower() == "нет":
            it["it2"] +=1
            await state.update_data(it2=it["it2"])
        await message.answer(config.questions_it[it["current_question_it"]])
        it["current_question_it"] += 1
        await state.update_data(current_question_it=it["current_question_it"])      
    else:
        await state.set_state(main_states.econom)
        await state.update_data(econom1=0)
        await state.update_data(econom2=0)
        await message.answer(config.questions_econom[0])
        await state.update_data(current_question_econom=1)

@router.message(main_states.econom, F.text.lower().in_({"да","нет"}))
async def economprocces(message: Message, state=FSMContext):
    econom =  await state.get_data()
    
    if econom["econom2"] < 4 and econom["current_question_econom"] < len(config.questions_econom):
        if message.text.lower() == "да":
            econom["econom1"] +=1
            await state.update_data(econom1=econom["econom1"])
        elif message.text.lower() == "нет":
            econom["econom2"] +=1
            await state.update_data(econom2=econom["econom2"])
        await message.answer(config.questions_econom[econom["current_question_econom"]],reply_markup=kb.started_kb)
        econom["current_question_econom"] += 1
        
        await state.update_data(current_question_econom=econom["current_question_econom"])      
        
    else:
        await state.set_state(main_states.result)
@router.message(main_states.result)
#функция подчета результата, собирает все в нужные данные в переменную в 1 блоке
#второй блок вычесляет тему с самым большим кол-вом ответов "да"
#3 блок находит подходящий вывод результата 
async def user_result(message: Message, state=FSMContext):
    data = await state.get_data()
    result = {}
    keys_to_extract= ["it1","tvorch1","tech1","econom1"]  #собирает только нужные ключи
    for key in keys_to_extract:
        if key in data:
            result[key] = data[key]
            
    maxvalue = float('-inf') # вычисляет ключ с самым большим колвом ответов "да"
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

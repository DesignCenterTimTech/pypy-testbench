# MyBrainFuck
Это маленький полуобучающий проект о том, как пользоваться PyPy на примере написания интерпрeтатора для языкa [brainfuck](https://ru.wikipedia.org/wiki/Brainfuck). Здесь мы напишем и проведем последовательное улучшение интерпретатора на Питоне. С более подробной информацией можно ознакомится [в статье на Хабре](https://habr.com/ru/post/124418/) а исходный код [в репозитории на Github](https://github.com/disjukr/pypy-tutorial-ko). Тут мы просто обобщаем и автоматизируем при помощи скриптов выполнение всех процессов и тестов. В качестве результата мы получим копилятор, который будет переводить код brainfuck в машинный код.
## Подготовка
Для начала нам понадобится `python3`,`pypy3.9` и `hg`. Чтобы проверить, если ли у вас эти программы пропишите следующие команды.
```
python --version
pypy --version
```
Ответ не должен содержать сообщения об ошибке. В обратном случае, делаем следующее:
```
sudo apt update
sudo apt install python3 pypy gcc mercurial
```
## Скрипты
Основные скрипты будут написаны в Makefile 
## Начало: интерпритатор на чистом питоне
Для начала написшем интерпретатор самостоятельно и запустим его с помощью питона. 
Если вам интересен код - можете заглянуть в папку `source`. Программы на brainfuck лежат в папке `brainfuck`, здесь мы запустим `first_brainfuck.b`.  Сейчас мы будем использовать файл `python_only.py`. Следующая команда:
```
make python_only 
```
После начнется падение 99 бутылок
## Первое улучшение: переходим на PyPy
Теперь перейдем к PyPy. Нам понадобится RPython, мы скачаем репозиторий с помощью следующей команды:
```
make install_pypy_rpython
```
Далее начнем трансляцию интерпретатора следующей командой
```
make simple_pypy
```
В результате мы получим папку build, в которой лежит наш интерпретатор, запустим его с программой, выводящей фрактал
```
cd build
time ./simple_pypy-c ../brainfuck/mandel.b 
cd ..
```
## Второе улучшение: добавляем JIT
Продолжим улучшение, воспользуемся фичей Pypy и добавим компилятор времени выполнения JIT. Для этого надо добавить несколько подсказок как в сам интерпретатор (сейчас это файл `jit_pypy.py`) и флагом для rpython
```
make jit_pypy
```
Он заметно дольше транслируется. Можно проверить результат слудующим образом:
```
cd build
time ./jit_pypy-c ../brainfuck/mandel.b 
cd ..
```
Будет выводиться фрактал, даже несколько быстрее чем в предыдущем случае.
## Третье улучшение: оптимизация
Добавим минорную оптимизацию. Мы скажем компилятору что dict не меняется в процессе использования его внутри mainloop.
```
make opt_jit_pypy
```
Ну и проверить это можно следующим способом:
```
cd build
time ./opt_jit_pypy-c ../brainfuck/mandel.b 
cd ..
```
## Результат
Теперь мы имеем 3 интерпретатора в папке build

## Бонус: Отладка и логи
Ну как можно обойтись без инструмента дебага, позволяющего нам видеть все необходимое. Здесь мы проапдейтим наш интрепретатор так, чтобы он при соблюдении определненых условий выводил отладочную информацию. Необходимые изменения можно найли в файле `log_jit_pypy.py`. Команда для вызова:
```
make log_jit_pypy
```
Теперь нам нужно установить переменную PYPYLOG для того, чтобы выводить определенные логи в определенный файл
```
export PYPYLOG=jit-log-opt:logfile 
```
далее запускаем программу, тут мы будем пользоваться тестовой маленькой программой 
```
cd build
./log_jit_pypy-c ../brainfuck/bench.b
cat logfile
```
Теперь мы можем анализировать результат работы программы с логами

## ViewCode

Для того чтобы запустить viewcode.py нам необходимы модули `py` и `pygame` для pypy2.7.
```
pypy -m pip install py pygame
```

Далее установим переменные среды.
```
export PYPYLOG=jit-backend-dump:log
export PYTHONPATH=`pwd`/pypy
```

Далле сгенерируем транслятор
```
make log_jit_pypy
```

Запускаем его
```
cd build
./log_jit_pypy-c ../brainfuck/mandel.b
```

Появится файл log, теперь можно сделать `viewcode.py`
```
cd ..
pypy pypy/rpython/jit/backend/tool/viewcode.py build/log
```

Или вы можетно запустить скрипт
```
make viewcode
```
## Вызов c-функции 
Данный раздел пока что использует отдельный код, для демонстрации работы вызова с-функии из динамической библеотеке.

Для начала необходимо сокмпилировать дин библеотеку с одной функцией:
```
void hello() {
	printf("Hello world!\n")
}
```
Это можно сделать следующим образом
```
cd source/csource
make
cd ../..
```
Далее запустим скрипт
```
make call_c_fun
```
## MrBrainFuck с вызовом функций
Теперь в языке добавлены новые символы
 * 'h' - выводит строку "Hello, world"
 * 'p' - выводит значение переменной 'position'
 * 'w' - выводит значение 42 (ответ на вселенский вопрос и вообще)

Если необходило скомпелировать и вызвать выполнение тестового скрипта, используйте следующую команду
```
make play_hellofun
```
Если в добавок необходимо еще и просмотреть дамп jit, используйте следющую команду
```
make viewcode_withfun
```
Если вы уже скомпилировали интерпритатор, то просто запустить работу программы можно следующей коммандой
```
make play_hellofun_only
```
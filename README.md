# MyBrainFuck
Это маленький полуобучающий проек как пользоваться PyPy на примере написания интерпритатора для языкa [brainfuck](https://ru.wikipedia.org/wiki/Brainfuck). Здесь мы напишем и проведем последовательное улучшение интерпритатора на Питоне. С более подробной информацией можно ознакомится [в статье на Хкбре](https://habr.com/ru/post/124418/) а исходный код [в репазитории на Github](https://github.com/disjukr/pypy-tutorial-ko). Тут мы просто обобщаем и автоматизируем при помощи скриптов выполнение всех процессов и тестов. В качестве результата мы получим копилятор, который будет переводить код brainfuck в машинный код.
## Подготовка
Для начала нам понадобиться `python3`,`pypy3.9` и `hg`. Чтобы проверить, если ли у вас эти программы пропишите следующий команды.
```
python --version
pypy --version
hg --version
```
Ответ не должен содержать сообщения об ошибке. В обратном случае, делаем следующее:
```
sudo apt update
sudo apt install python3 pypy hg gcc
```
## Скрипты
Основные скрипты будут написаны в Makefile 
## Начало: интерпритатор на чистом питоне
Для начала написшем интерпритатор самостоятельно и запустим его с помощью питона. 
Если вам интересен код можете заглянуть в папку `examples`. Программы на brainfuck лежит в папке `test_brainfuck`, здесь мы запустим `first_brainfuck.b`.  Сейчас мы будем использовать файл `python_only.py`. Следующая команда:
```
make python_only 
```
После начнется падение 99 бутылок
## Первое улучшение: переходим на PyPy
Теперь перейдем к PyPy. Нам понадобиться RPython, мы скачаем репазиторий с помощью следующей команды:
```
make install_pypy_rpython
```
Далее начнем трансляцию интерпритатора следующей командой
```
make simple_pypy
```
В результате мы получим папку build, в которой лежит наш интерпритатор, запустим его с программой, выводящей фрактал
```
cd build
./simple_pypy-c ../brainfuck/mandel.b 
cd ..
```
## Второе улучшение: добавляем JIT
Продолжим улучшение, воспользуемся фичей Pypy и добавим компилятор времени выполнение JIT. Для этого надо добавить несколько подсказак как в сам интрепритатор (сейчас это файл `jit_pypy.py`) и флагом для rpython
```
make jit_pypy
```
Он заметно дольше транслируется. Можно проверить результат слудующим образом:
```
cd build
./jit_pypy-c ../brainfuck/mandel.b 
cd ..
```
Буду вывадтся фрактал, даже несколько быстрее чем в предыдущем случае.
## Третье улучшение: оптимизация
Добавим минорную оптимизацию. Мы скажем компилятору что dict не меняется в процессе использования его внутри mainloop.
```
make opt_jit_pypy
```
Ну и проверить это можно следующим способом:
```
cd build
./opt_jit_pypy-c ../brainfuck/mandel.b 
cd ..
```
## Результат
Теперь мы имеем 3 интерпритатора в папке build

## Бонус: Отладка и логи
Ну как можно обойтись без инструмента дебага, позволяющего нам видеть все необходимое. Здесь мы проабдейтим на интрепритатор так, чтобы он при соблюдении определнных условий выводил дебаг информацию. необходимые изменения можно найли в шайле `log_jit_pypy.py`. Команда для вызова:
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
./log_jit_pypy ../brainfuck/bench.b
cat logfile
```

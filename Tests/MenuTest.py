from sugar import Menu, clear

menu = Menu()
clear()
menu.print_menu("Bem-vindo à cabeça da Laika. Escolha a opção que deseja.", ["caçar rato", "comer", "dormir", "azunhar"], incorrect_message="Você digitou uma opção inválida.", selectors="greek_alphabet")
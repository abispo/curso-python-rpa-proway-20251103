# Selenium

## O que é Selenium?

O **Selenium** é uma suite de ferramentas open-source para automação de navegadores web, amplamente utilizada em testes de software e processos de RPA (Robotic Process Automation).

## Por que usar Selenium em RPA?

- **Automatiza interações web**: Preenchimento de formulários, cliques, navegação
- **Suporte a múltiplos navegadores**: Chrome, Firefox, Edge, etc.
- **Linguagens variadas**: Python, Java, C#, JavaScript
- **Simula ações humanas**: Ideal para processos repetitivos em navegadores

## Componentes Principais

- **Selenium WebDriver**: API para controle direto do navegador
- **Selenium IDE**: Gravador de macros para testes
- **Selenium Grid**: Execução paralela em múltiplas máquinas

# Desafio

- Você irá acessar o site `https://saucedemo.com`, e efetuar o login (pode usar os nomes de usuários e senha que estão informados na própria página)
- Depois que logar no site, você irá colocar 2 itens no carrinho, e depois irá acessar o carrinho.
- Após isso, irá clicar no botão checkout e preencher as informações no formulário.
- Depois das informações preenchidas, você irá clicar no botão Continue.
- Após isso você irá para a página de visualização do checkout.
- Você deve mostrar no terminal os itens que você colocou no carrinho, os valores de `Payment Information` e `Shipping Information` e por final o preço total, com a taxa inclusa.
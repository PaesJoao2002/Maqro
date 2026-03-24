# Maqro - Gerador de QR Code
Maqro é um software que gera QR Codes offline para as mais diversas finalidades, desde redirecionamento em sites até para pagamentos via pix. É um software baseado em Python que preza a simplicidade e dinamicidade. Apresenta uma interface minimalista porém extremamente eficaz, podendo ser carregado facilmente em computadores antigos.

[Documentação do Software](https://github.com/PaesJoao2002/Maqro/blob/main/Documenta%C3%A7%C3%A3o%20Maqro.pdf)

## Texto
QR Codes simples carregam apenas texto e nada mais. Podem carregar uma mensagem como "Um abraço do querido amigo", citações como ""Seja a diferença que gostaria de ver no mundo" - Mahatma Gandhi" ou instruções, principalmente para economizar espaço em impressões. Basta digitar seu texto no campo de entrada e clicar em **Gerar/Atualizar**.

## Redirecionamento
Redirecionar usuários para outros sites é extremamente fácil. Basta colar sua URL no campo de entrada e **Gerar/Atualizar** para gerar um QR Code que leva o usuário diretamente para o site desejado. Não sendo necessário colocar "https://" no começo da url, pois o próprio programa se encarregará disso.

## Pix
Gerar QR Codes para chaves Pix é prático e seguro. Você pode fornecer um QR Code para seus clientes realizarem pagamentos em sua conta bancária utilizando chaves como telefone, e-mail, chave aleatória, CPF ou até seu CNPJ. O Software oferece suporte para gerar QR codes corretos facilmente.

## Customização
Opcionalmente, o usuário pode customizar seu QR Code, inserindo o logotipo da empresa, símbolos para fácil identificação do propósito do QR Code ou alterando cores para sua preferência. (No momento, o programa apenas oferece suporte a customização de logotipo e cores.)

## Exportação
Você pode exportar seu QR Code ao clicar no botão "Exportar", abaixo do QR Code gerado. No momento, há apenas suporte para exportar imagens em formato .PNG.

# Lista de afazeres (1.2)
- Aumentar suporte a um leque maior de opções de customização como mudança do formato de pontos (Mudar para círculos ou quadrados segmentados) e dos olhos do QR Code (As partes quadradas fechadas dos cantos do QR Code, formalmente chamados de PDP (Position Detection Pattern))
- Aumentar suporte a formatos de imagens para exportação como .SVG e .JPG
- Adicionar mais temas (talvez até customização de temas)
- Possibilitar a geração de outros tipos de códigos binários bidimensionais como data matrix.

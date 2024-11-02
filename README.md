# rad-python-pr

Projeto da Disciplina - Sistema de Gerenciamento de Expedição Espacial

> [!IMPORTANT]
> O relatório RAD do projeto esta disponível na pasta: /docs/RelatorioRAD.pdf

## **Comandos para execução da API**

1. **realizar a instalação das dependencias**
```
python -m pip install -r .\resources\requirements.txt
```

2. **criar a pasta env**
```
python -m venv env
```

3. **ativar os recuros**
```
.\env\Scripts\activate
```

4. **executar a aplicação**
```
python main.py
```

## **Endpoints da API**

### **1. `POST /missions/add`**
Adiciona uma nova missão ao sistema.

- **Corpo da Requisição**:
  ```json
  {
    "name": "Apollo 11",
    "launchDate": "1969-07-16",
    "destination": "Moon",
    "status": "completed",
    "crew": "Neil Armstrong, Buzz Aldrin",
    "payload": "Lunar Module",
    "duration": "8 days",
    "cost": 1000000.0,
    "missionInfo": "First manned mission to the moon"
  } 
  ```

- **Campos obrigatórios**:
  - `name` (string)
  - `launchDate` (string, formato: "YYYY-MM-DD")
  - `destination` (string)
  - `missionStatus` (string, valor do enum `MissionStatus`)
  - `cost` (float)

- **Resposta de Sucesso**:
  ```json
  {
    "message": "Mission created successfully!",
    "id": 11
  }
  ```

### **2. `GET /missions/get`**
Busca missões com base no intervalo de datas fornecido.

- **Parâmetros de Query**:
  ```json
  {
    "startDate": "1969-07-16",
    "endDate": "1969-07-16"
  }
  ```

- **Campos obrigatórios**:
  - `startDate` (string, formato: "YYYY-MM-DD")
  - `endDate` (string, formato: "YYYY-MM-DD")

- **Resposta de Sucesso**:
  ```json
  [
    {
      "id": 11,
      "name": "Apollo 11",
      "launchDate": "1969-07-16",
      "destination": "Moon",
      "status": "completed",
      "crew": "Neil Armstrong, Buzz Aldrin",
      "payload": "Lunar Module",
      "duration": "8 days",
      "cost": "1000000.00",
      "missionInfo": "First manned mission to the moon"
    }
  ]
  ```

### **3. `PUT /missions/update/<int:mission_id>`**
Atualiza os dados de uma missão específica.

- **Parametros obrigatório**:
  - `id` (int)

- **Corpo da Requisição**:
  ```json
  {
    "name": "Nome da missão (opcional)",
    "launchDate": "YYYY-MM-DD (opcional)",
    "destination": "Destino da missão (opcional)",
    "status": "Status da missão (opcional)",
    "crew": "Tripulação da missão (opcional)",
    "payload": "Carga útil da missão (opcional)",
    "duration": "Duração da missão (opcional)",
    "cost": 12345.67,
    "missionInfo": "Informações adicionais sobre a missão (opcional)"
  }
  ```

- **Resposta de Sucesso**:
  ```json
  {
    "message": "Mission updated successfully!"
  }
  ```

### **5. `DELETE /missions/delete/<int:mission_id>`**
Remove uma missão específica do sistema.

- **Parametros obrigatório**:
  - `id` (int)

- **Resposta de Sucesso**:
  ```json
  {
    "message": "Mission deleted successfully!"
  }
  ```


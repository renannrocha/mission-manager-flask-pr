# rad-python-pr

Projeto da Disciplina - Sistema de Gerenciamento de Expedição Espacial

Aqui está a documentação para cada endpoint com os campos necessários para os bodys:

---

## **Endpoints da API**

### **1. `POST /missions/add`**
Adiciona uma nova missão ao sistema.

- **Corpo da Requisição**:
  ```json
  {
    "name": "Nome da missão",
    "launchDate": "YYYY-MM-DD",
    "destination": "Destino da missão",
    "missionStatus": "Status da missão (ACTIVE, COMPLETED, etc.)",
    "crew": "Tripulação da missão",
    "payload": "Carga útil da missão",
    "duration": "Duração da missão",
    "cost": 12345.67,
    "missionInfo": "Informações adicionais sobre a missão"
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
    "id": "ID da missão criada"
  }
  ```

### **2. `GET /missions/get`**
Busca missões com base no intervalo de datas fornecido.

- **Parâmetros de Query**:
  ```json
  {
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD"
  }
  ```

- **Campos obrigatórios**:
  - `startDate` (string, formato: "YYYY-MM-DD")
  - `endDate` (string, formato: "YYYY-MM-DD")

- **Resposta de Sucesso**:
  ```json
  [
    {
      "id": "ID da missão",
      "name": "Nome da missão",
      "launchDate": "YYYY-MM-DD",
      "destination": "Destino da missão",
      "missionStatus": "Status da missão",
      "crew": "Tripulação da missão",
      "payload": "Carga útil da missão",
      "duration": "Duração da missão",
      "cost": 12345.67,
      "missionInfo": "Informações adicionais sobre a missão"
    }
  ]
  ```

### **3. `GET /missions/getById`**
Busca uma missão específica com base no ID.

- **Parâmetros de Query**:
  ```json
  {
    "id": "ID da missão"
  }
  ```

- **Campo obrigatório**:
  - `id` (int)

- **Resposta de Sucesso**:
  ```json
  {
    "id": "ID da missão",
    "name": "Nome da missão",
    "launchDate": "YYYY-MM-DD",
    "destination": "Destino da missão",
    "missionStatus": "Status da missão",
    "crew": "Tripulação da missão",
    "payload": "Carga útil da missão",
    "duration": "Duração da missão",
    "cost": 12345.67,
    "missionInfo": "Informações adicionais sobre a missão"
  }
  ```

### **4. `PUT /missions/update`**
Atualiza os dados de uma missão específica.

- **Corpo da Requisição**:
  ```json
  {
    "id": "ID da missão a ser atualizada",
    "name": "Nome da missão (opcional)",
    "launchDate": "YYYY-MM-DD (opcional)",
    "destination": "Destino da missão (opcional)",
    "missionStatus": "Status da missão (opcional)",
    "crew": "Tripulação da missão (opcional)",
    "payload": "Carga útil da missão (opcional)",
    "duration": "Duração da missão (opcional)",
    "cost": 12345.67,
    "missionInfo": "Informações adicionais sobre a missão (opcional)"
  }
  ```

- **Campo obrigatório**:
  - `id` (int)

- **Resposta de Sucesso**:
  ```json
  {
    "message": "Mission updated successfully!"
  }
  ```

### **5. `DELETE /missions/delete`**
Remove uma missão específica do sistema.

- **Corpo da Requisição**:
  ```json
  {
    "id": "ID da missão a ser deletada"
  }
  ```

- **Campo obrigatório**:
  - `id` (int)

- **Resposta de Sucesso**:
  ```json
  {
    "message": "Mission deleted successfully!"
  }
  ```

---

Essas documentações permitem que cada endpoint seja utilizado corretamente, especificando os campos obrigatórios e opcionais, bem como os formatos esperados e as respostas de sucesso.
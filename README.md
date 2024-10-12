# wide-column-store
Projeto 2 - Tópicos avançados de banco de dados 

## Alunas  

- Aléxia Suares  RA:
- Gabrielle Mitie   RA: 22.124.097-1
- Larissa Gonçalves   RA: 22.224.



## Descrição das coleções utilizadas  


CREATE TABLE Curso (  
    id_curso INT PRIMARY KEY,   
    nome_curso TEXT  
);  




CREATE TABLE Aluno (  
    RA INT PRIMARY KEY,  
    nome_aluno TEXT,  
    ano_matricula INT,  
    id_curso INT,  
    codigo_disc INT  
);    




CREATE TABLE Disciplina (  
    codigo_disc INT PRIMARY KEY,  
    nome_disc TEXT,  
    ano_disc INT,  
    semestre_disc INT,  
    codigo_prof INT,  
    id_curso INT  
);   





CREATE TABLE MatrizCurricular (  
    id_matriz INT,  
    semestre_aprovado INT,  
    ano_aprovado INT,  
    id_curso INT,  
    codigo_disc INT,  
    PRIMARY KEY (id_matriz, codigo_disc)  
);   



CREATE TABLE HistEsc (  
    RA INT,  
    codigo_disc INT,  
    nota DECIMAL,  
    semestre_cursado INT,  
    ano_cursado INT,  
    PRIMARY KEY (RA, codigo_disc)  
);   


CREATE TABLE HistDisc (  
    codigo_prof INT,   
    codigo_disc INT,  
    ano_ministrado INT,  
    semestre_ministrado INT,  
    PRIMARY KEY (codigo_prof, codigo_disc)  
);   


CREATE TABLE Departamento (  
    nome_dep TEXT PRIMARY KEY,  
    codigo_dep TEXT,  
    nome_prof TEXT,  
    codigo_disc INT,  
    id_curso INT  
);   


CREATE TABLE Professor (
    codigo_prof INT PRIMARY KEY,  
    nome_prof TEXT,  
    chefe_dep BOOLEAN,  
    id_curso INT  
);








CREATE TABLE historico_aluno AS 
SELECT 
        histesc.codigo_disc, 
        disciplina.nome_disc, 
        histesc.semestre_cursado, 
        histesc.ano_cursado, 
        histesc.nota, 
        aluno.nome_aluno, 
        aluno.ra
    FROM 
        histesc
    INNER JOIN aluno ON histesc.ra = aluno.ra
    INNER JOIN disciplina ON histesc.codigo_disc = disciplina.codigo_disc;

CREATE TABLE historico_prof AS
SELECT 
        professor.id_curso, 
        professor.nome_prof, 
        disciplina.nome_disc, 
        disciplina.semestre_disc,  
        disciplina.ano_disc, 
        professor.codigo_prof
    FROM 
        disciplina
    INNER JOIN professor ON disciplina.codigo_prof = professor.codigo_prof;

CREATE TABLE chef_dep AS
SELECT 
        professor.nome_prof,
        professor.codigo_prof,
        professor_departamento.nome_dep
    FROM
        professor
    INNER JOIN professor_departamento ON professor.codigo_prof = professor_departamento.codigo_prof
    WHERE professor.chefe_dep = TRUE;


CREATE TABLE grupos_tcc AS 
SELECT 
        professor.codigo_prof, 
        professor.nome_prof, 
		aluno.nome_aluno,  
        aluno.id_tcc, 
        aluno.ra
    FROM 
        aluno
    INNER JOIN professor ON professor.id_tcc = aluno.id_tcc;

CREATE TABLE alunos_formados AS 
SELECT 
		aluno.nome_aluno,   
        aluno.ra,
		matrizcurricular.id_matriz,
		curso.id_curso,
		curso.nome_curso,
		matrizcurricular.ano_aprovado,
		matrizcurricular.semestre_aprovado
    FROM aluno
    JOIN formados ON formados.ra = aluno.ra
	JOIN matrizcurricular ON matrizcurricular.id_matriz = formados.id_matriz
	JOIN curso ON curso.id_curso = matrizcurricular.id_curso;

ALTER TABLE historico_aluno
ADD PRIMARY KEY (ra, codigo_disc);

ALTER TABLE historico_prof
ADD PRIMARY KEY (codigo_prof);

ALTER TABLE chef_dep
ADD PRIMARY KEY (codigo_prof);

ALTER TABLE grupos_tcc
ADD COLUMN id SERIAL PRIMARY KEY;

ALTER TABLE alunos_formados
ADD PRIMARY KEY (ra, id_matriz, id_curso);



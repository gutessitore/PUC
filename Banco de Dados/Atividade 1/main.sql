.header on
.mode column


CREATE TABLE curso (
  nome TEXT,
  duracao_anos INTEGER,
  carga_horaria INTEGER,
  id INTEGER primary key 
);


CREATE TABLE disciplina (
  nome TEXT,
  codigo TEXT,
  ano INTEGER,
  id_curso INTEGER KEY REFERENCES curso(id)
);


INSERT INTO disciplina VALUES
  ('Introdução ao direito', 'D001', 1, 1),
  ('Direito Digital', 'D034', 2, 1),
  ('Direito do Trabalho', 'D009', 3, 1),
  ('Direito na LGPD', 'D120', 4, 1),
  ('Ética', 'D921', 5, 1),
  ('Introdução ao Pensamento Computacional', 'CC001', 1, 2),
  ('Sociedade Digital', 'CC34', 2, 2),
  ('Programação JAVA', 'CC009', 3, 2),
  ('Banco de Dados', 'CC120', 4, 2),
  ('Ética', 'CC921', 4, 2);

INSERT INTO curso VALUES
  ('Direito', 5, 4000, 1),
  ('Ciência da Computação', 4, 3200, 2);

-- SELECT * FROM disciplina;
-- .print ''
-- SELECT * FROM curso;


.print ''
.print 'Listando os cursos'
select 
  nome 
from curso;


.print ''
.print 'Listar as disciplinas de cada curso'
select 
  c.nome as nome_curso
  ,d.nome as nome_disciplina
from curso as c
  INNER JOIN disciplina as d
    ON c.id = d.id_curso;


.print ''
.print 'Exibir o número de disciplinas de cada curso'
select 
  c.nome as nome_curso
  ,COUNT(d.codigo) as numero_disciplinas
from curso as c
  INNER JOIN disciplina as d
    ON c.id = d.id_curso
GROUP BY d.id_curso;


.print ''
.print 'Lista as disciplinas do 1 ano'
select 
  nome 
from disciplina
where ano = 1;


.print ''
.print 'Listar os cursos que são de 4 anos'
select 
  nome 
from curso 
where duracao_anos = 4;
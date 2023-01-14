-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: lattes4web
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `projetos`
--

DROP TABLE IF EXISTS `projetos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projetos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `titulo` text,
  `ano_inicio` varchar(4) NOT NULL,
  `natureza` varchar(100) DEFAULT NULL,
  `coordenador` varchar(255) DEFAULT NULL,
  `financiamento` text NOT NULL,
  `integrantes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
INSERT INTO `projetos` VALUES (1,'Aldebaro Barreto da Rocha Klautau J├║nior','Processamento de Sinais em Telecomunica├º├Áes e Monitoramento com Implementa├º├Áes em FPGA e Sil├¡cio','2014','PESQUISA','Aldebaro Barreto da Rocha Klautau J├║nior','Conselho Nacional de Desenvolvimento Cient├¡fico e Tecnol├│gico','Aldebaro Barreto da Rocha Klautau J├║nior'),(2,'Aldebaro Barreto da Rocha Klautau J├║nior','Telefonia Celular Comunit├íria - CELCOM','2016','EXTENSAO','Aldebaro Barreto da Rocha Klautau J├║nior','Secretaria de Ci├¬ncia, Tecnologia e Educa├º├úo do Estado do Par├í, Universidade Federal do Par├í','Aldebaro Barreto da Rocha Klautau J├║nior, Felipe Henrique Bastos e Bastos, Jeferson Breno Negr├úo Leite, Sandoval Silva Oliveira Junior, Cleverson Veloso Nahum, Bruno Ricardo Scherer, Larissa Guimar├úes Nogueira, Caio de Jesus Semblano Martins, Pedro Batista, Ivanes Lian Costa Araujo'),(3,'Aldebaro Barreto da Rocha Klautau J├║nior','UFA22-Intelig├¬ncia Artificial Conectada para Redes 5g com Aplica├º├Áes de Vis├úo Computacional','2019','PESQUISA','Aldebaro Barreto da Rocha Klautau J├║nior','Ericsson Telecomunica├º├Áes - Matriz','GOMES, DIEGO, Emerson Santos de Oliveira Junior, BRITO, FLAVIO, Bruno Ricardo Scherer, Tiago da Silva Guerreiro, Caio de Jesus Semblano Martins, KAIO HENRIQUE SINIMBU FORTE, CARNOT LUIZ BRAUN GUIMAR├âES FILHO, Virginia Brioso Tavares, Felipe Henrique Bastos e Bastos, Jeferson Breno Negr├úo Leite, Cleverson Veloso Nahum, Thiago Lima Sarmento, Carlos EduardoD. Vinagre neto, Pedro Batista, Lucas dos Santos Conde, Lauro Brito de Castro, Yuri Souza da Silva, CORREA, Ilan S, Diego Dantas, Lucas Damasceno Silva, Ingrid Nascimento, Luan Gon├ºalves de Assis, Andrey Silva, Ivanes Lian Costa Araujo, Aldebaro Barreto da Rocha Klautau J├║nior, Leonardo Lira Ramalho, Igor Ant├┤nio Auad Freire, Sandoval Silva Oliveira Junior, MULLER, FRANCISCO C. B. F., Pedro Bemerguy, Lucas Pinto, Larissa Guimar├úes Nogueira, Jamelly Freitas Ferreira'),(4,'Aldebaro Barreto da Rocha Klautau J├║nior','Uso de Redes Neurais Recorrentes para Modelagem de L├¡ngua em Reconhecimento de Fala em Portugu├¬s Brasileiro com o Kaldi','2019','PESQUISA','Nelson Cruz Sampaio Neto','','GOMES, DIEGO, Emerson Santos de Oliveira Junior, BRITO, FLAVIO, Bruno Ricardo Scherer, Tiago da Silva Guerreiro, Caio de Jesus Semblano Martins, KAIO HENRIQUE SINIMBU FORTE, CARNOT LUIZ BRAUN GUIMAR├âES FILHO, Virginia Brioso Tavares, Felipe Henrique Bastos e Bastos, Joao Victor da Silva Dias Canavarro, Jeferson Breno Negr├úo Leite, Nelson Cruz Sampaio Neto, Cleverson Veloso Nahum, Thiago Lima Sarmento, Carlos EduardoD. Vinagre neto, Pedro Batista, Lucas dos Santos Conde, Lauro Brito de Castro, Yuri Souza da Silva, CORREA, Ilan S, Diego Dantas, Lucas Damasceno Silva, Ingrid Nascimento, Luan Gon├ºalves de Assis, Andrey Silva, Ivanes Lian Costa Araujo, Aldebaro Barreto da Rocha Klautau J├║nior, Leonardo Lira Ramalho, Igor Ant├┤nio Auad Freire, Sandoval Silva Oliveira Junior, MULLER, FRANCISCO C. B. F., Pedro Bemerguy, Lucas Pinto, Larissa Guimar├úes Nogueira, Jamelly Freitas Ferreira'),(5,'Antonio Jorge Gomes Abel├®m','Gest├úo Inteligente do Parque de Ci├¬ncia e Tecnologia Guam├í - PCT GUAM├ü','2012','DESENVOLVIMENTO','Antonio Jorge Gomes Abel├®m','Financiadora de Estudos e Projetos','Antonio Jorge Gomes Abel├®m'),(6,'Antonio Jorge Gomes Abel├®m','Solu├º├úo Descentralizada de Virtualiza├º├úo para Redes Definidas por Software','2018','DESENVOLVIMENTO','Antonio Jorge Gomes Abel├®m','Conselho Nacional de Desenvolvimento Cient├¡fico e Tecnol├│gico','Antonio Jorge Gomes Abel├®m, Fernando Nazareno Nascimento Farias, Ant├┤nio de Oliveira Junior'),(7,'Filipe de Oliveira Saraiva','M├®todos Metaheur├¡sticos e Intelig├¬ncia Computacional para Otimiza├º├úo, Modelagem e Simula├º├Áes de Sistemas El├®tricos de Pot├¬ncia e Redes El├®tricas Inteligentes','2016','PESQUISA','Filipe de Oliveira Saraiva','','Filipe de Oliveira Saraiva, Kelly do Socorro Silva da Costa, Jeanne de Oliveira Pereira, Ronaldd Patrik Silva Pinho, Camil Samer Zahlan Redwan, Renan Lobo Duarte, Italo Ramon da Costa Campos, Marcos Venicios Correa de Sousa, Necy de Nazar├® Corr├¬a Trindade, Rafael de Souza Cavalheiro'),(8,'Filipe de Oliveira Saraiva','Centro de Compet├¬ncia em Software Livre da UFPA','2018','EXTENSAO','Filipe de Oliveira Saraiva','Universidade Federal do Par├í','Filipe de Oliveira Saraiva, Kelly do Socorro Silva da Costa, J├®ssica Herzog Viana, Jeanne de Oliveira Pereira, Ronaldd Patrik Silva Pinho, Camil Samer Zahlan Redwan, Renan Lobo Duarte, Leonardo Ribeiro da Cruz, Gustavo Henrique Lima Pinto, Italo Ramon da Costa Campos, Marcos Venicios Correa de Sousa, Necy de Nazar├® Corr├¬a Trindade, Luiz Henrique Worthington Maia Dores, Tel Amiel, Rafael de Souza Cavalheiro, Lucas Gabriel De Souza, Paulo Victor Lobato Sarmento'),(9,'Filipe de Oliveira Saraiva','Compreendendo o Papel dos Eventos Colaborativos de Curta Durac&#807;a&#771;o na Economia Digital','2020','PESQUISA','Gustavo Henrique Lima Pinto','Conselho Nacional de Desenvolvimento Cient├¡fico e Tecnol├│gico','Filipe de Oliveira Saraiva, Marcos Venicios Correa de Sousa, Tel Amiel, Rafael de Souza Cavalheiro, J├®ssica Herzog Viana, Ronaldd Patrik Silva Pinho, Renan Lobo Duarte, Italo Ramon da Costa Campos, Necy de Nazar├® Corr├¬a Trindade, Luiz Henrique Worthington Maia Dores, Leonardo Ribeiro da Cruz, Sandro Ronaldo Bezerra Oliveira, Maria Iracilda da Cunha Sampaio, Gustavo Henrique Lima Pinto, Lucas Gabriel De Souza, Paulo Victor Lobato Sarmento, Kelly do Socorro Silva da Costa, Jeanne de Oliveira Pereira, Camil Samer Zahlan Redwan, Cleidson Ronald Botelho de Souza'),(10,'Filipe de Oliveira Saraiva','Aplicativo M├│vel para Roteiro Geo-Tur├¡stico em Bel├®m','2020','EXTENSAO','Filipe de Oliveira Saraiva','Universidade Federal do Par├í','Filipe de Oliveira Saraiva, Marcos Venicios Correa de Sousa, Tel Amiel, Rafael de Souza Cavalheiro, J├®ssica Herzog Viana, Ronaldd Patrik Silva Pinho, Renan Lobo Duarte, Italo Ramon da Costa Campos, Vinicius Chaves Botelho, Necy de Nazar├® Corr├¬a Trindade, Luiz Henrique Worthington Maia Dores, Leonardo Ribeiro da Cruz, Sandro Ronaldo Bezerra Oliveira, Maria Iracilda da Cunha Sampaio, Gustavo Henrique Lima Pinto, Lucas Gabriel De Souza, Paulo Victor Lobato Sarmento, Kelly do Socorro Silva da Costa, Jeanne de Oliveira Pereira, Camil Samer Zahlan Redwan, Cleidson Ronald Botelho de Souza'),(11,'Gustavo Henrique Lima Pinto','Compreendendo o Papel dos Eventos Colaborativos de Curta Durac&#807;a&#771;o na Economia Digital','2020','PESQUISA','Gustavo Henrique Lima Pinto','Conselho Nacional de Desenvolvimento Cient├¡fico e Tecnol├│gico','Gustavo Henrique Lima Pinto, Cleidson Ronald Botelho de Souza, Filipe Saraiva, Sandro Bezerra, Maria Iracilda da Cunha Sampaio'),(12,'Roberto Samarone dos Santos Ara├║jo','Pesquisa e Desenvolvimento de Protocolo para Vota├º├Áes Seguras','2011','PESQUISA','Roberto Samarone dos Santos Ara├║jo',', Rede Nacional de Ensino e Pesquisa','Felipe Leite, Lucas Melo Silva, Leonardo Sarraf Nunes Moraes, Dionne Cavalcante Monteiro, Roberto Samarone dos Santos Ara├║jo');
/*!40000 ALTER TABLE `projetos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resultados`
--

DROP TABLE IF EXISTS `resultados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_docente` varchar(255) NOT NULL,
  `documento` varchar(20) NOT NULL,
  `ano_evento` varchar(4) NOT NULL,
  `titulo` text NOT NULL,
  `doi` varchar(100) NOT NULL,
  `sigla` varchar(20) NOT NULL,
  `nome_evento` text NOT NULL,
  `autores` text NOT NULL,
  `estratos` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `notas` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resultados`
--

LOCK TABLES `resultados` WRITE;
/*!40000 ALTER TABLE `resultados` DISABLE KEYS */;
INSERT INTO `resultados` VALUES (1,'MARCELLE PEREIRA MOTA','Conferencia','2017','A Study on Knowledge Transfer Between Programming Languages by Programs Meanings Facets','10.1145/3160504.3160530','IHC','Brazilian Symposium on Human Factors in Computing Systems','BARATA, PABLO EDUARDO CABRAL/ CORR├èA, JO├âO VICTOR P./ Marcelle Pereira Mota','B1','0.5'),(2,'MARCELLE PEREIRA MOTA','Conferencia','2017','Analyzing the benefits of the combined interaction of head and eye tracking in 3D visualization information','10.1145/3160504.3160532','IHC','the XVI Brazilian Symposium','FREITAS, ALEXANDRE A./ ARA├ÜJO, TIAGO D. O./ JUNIOR, PAULO R. S. C./ MIRANDA, BRUNELLI P./ MURAKAMI, BRUNO A. F./ SANTOS, CARLOS G. R./ Marcelle Pereira Mota/ MEIGUINS, BIANCHI S.','B1','0.5'),(3,'MARCELLE PEREIRA MOTA','Conferencia','2017','Virtualiza├º├úo de monumentos em dispositivos m├│veis: Relato do desenvolvimento e Avalia├º├úo de um Ambiente de Patrim├┤nio Virtual e Turismo Ub├¡quo','-','-','XVI Escola Regional de Inform├ítica Norte 2','Jefferson Pantoja/ Carmem Silva/ Marcelle Pereira Mota','-','SEM QUALIS'),(4,'MARCELLE PEREIRA MOTA','Conferencia','2018','Adaptation and Automation of a Cancellation Test for Evaluation of Exploratory Visual Behavior','10.1145/3274192.3274197','IHC','the 17th Brazilian Symposium','CASCAES, RENATA/ LAMEIRA, KALILL/ SARMANHO, RICARDO/ PINHEIRO, KELLY/ Marcelle Pereira Mota/ PEREIRA, ANT├öNIO/ NETO, NELSON CRUZ SAMPAIO','B1','0.5'),(5,'MARCELLE PEREIRA MOTA','Conferencia','2018','Usability Considerations For Coercion-Resistant Election Systems','10.1145/3274192.3274232','IHC','the 17th Brazilian Symposium','NETO, ANDR├ë SILVA/ LEITE, MATHEUS/ ARA├ÜJO, ROBERTO/ Marcelle Pereira Mota/ NETO, NELSON CRUZ SAMPAIO/ TRAOR├ë, JACQUES','B1','0.5'),(6,'MARCELLE PEREIRA MOTA','Conferencia','2019','Proposal and Evaluation of Textual Description Templates for Bar Charts Vocalization','10.1109/IV.2019.00036','IV','2019 23rd International Conference Information Visualisation (IV)','TELES DE OLIVEIRA, CYNTHYA LETICIA/ SILVA, ALAN TRINDADE DE ALMEIDA/ CAMPOS, ERICK MODESTO/ ARAUJO, TIAGO DAVI OLIVEIRA/ Marcelle Pereira Mota/ MEIGUINS, BIANCHI SERIQUE/ MORAIS, JEFFERSON MAGALHAES DE','A4','0.625'),(7,'MARCELLE PEREIRA MOTA','Conferencia','2019','UXmood - A Tool to Investigate the User Experience (UX) Based on Multimodal Sentiment Analysis and Information Visualization (InfoVis)','10.1109/iv.2019.00038','IV','2019 23rd International Conference Information Visualisation (IV)','DA SILVA FRANCO, ROBERTO YURI/ ABREU DE FREITAS, ALEXANDRE/ SANTOS DO AMOR DIVINO LIMA, RODRIGO/ Marcelle Pereira Mota/ RESQUE DOS SANTOS, CARLOS GUSTAVO/ SERIQUE MEIGUINS, BIANCHI','A4','0.625'),(8,'MARCELLE PEREIRA MOTA','Conferencia','2019','A study on customizing interaction in adaptable games','10.1145/3357155.3358468','-','the 18th Brazilian Symposium','DE CARVALHO, CAIO PINHEIRO/ SANTOS, SUZANE SANTOS DOS/ DE MAGALH├âES ESCUDEIRO, GABRIEL/ PINHEIRO, KELLY VALE/ NETO, NELSON CRUZ SAMPAIO/ Marcelle Pereira Mota','B1','0.5'),(9,'MARCELLE PEREIRA MOTA','Conferencia','2019','Cuca Fresca: Estudo de Caso de um Jogo da Mem├│ria S├®rio Adapt├ível','-','SBGAMES','Simp├│sio Brasileiro de Jogos e Entretenimento Digital (SBGames)','Caio Pinheiro de Carvalho/ Gabriel Magalh├úes Escudeiro/ PINHEIRO, KELLY VALE/ Marcelle Pereira Mota','B1','0.5'),(10,'MARCELLE PEREIRA MOTA','Conferencia','2020','Um Modelo para Auxiliar a Descoberta e Classifica├º├úo de Conte├║do para Ambientes Virtuais de Aprendizagem','-','COTB','Computer on the beach','Rafael Martins Feitosa/ Cleyton Aparecido Dim/ Marcelle Pereira Mota/ Jefferson Magalh├úes de Morais/ Raimundo Viegas Junior/ Orlando Belo','B3','0.1'),(11,'MARCELLE PEREIRA MOTA','Conferencia','2020','A Smartphone Application for Car Horn Detection to Assist Hearing-Impaired People in Driving','-','ICCSA','Computational Science and Its Applications','Cleyton Aparecido Dim/ Rafael Martins Feitosa/ Marcelle Pereira Mota/ Jefferson Magalh├úes de Morais','A3','0.75'),(12,'MARCELLE PEREIRA MOTA','Conferencia','2020','LocaLibras: An Inclusive Geolocation Application','-','IHC','XIX Simp├│sio Brasileiro sobre Fatores Humanos em Sistemas Computacionais','Samara Fernandes Pimentel/ Paulo Weskley de Almeida Ferreira/ Luciano Arruda Teran/ Marcelle Pereira Mota','B1','0.5'),(13,'MARCELLE PEREIRA MOTA','Conferencia','2020','ChartVision: Accessible Vertical Bar Charts','-','IHC','XIX Simp├│sio Brasileiro sobre Fatores Humanos em Sistemas Computacionais','Cynthya Let├¡cia Teles de Oliveira/ Alan Trindade de Almeida Silva/ Jefferson Magalh├úes de Morais/ Marcelle Pereira Mota','B1','0.5'),(14,'MARCELLE PEREIRA MOTA','Conferencia','2020','On the Study of Visual Exploration vs. Educational Levels Using an Automated Cancellation Test','-','IHC','XIX Simp├│sio Brasileiro sobre Fatores Humanos em Sistemas Computacionais','Suzane Santos dos Santos/ Erick Modesto Campos/ Paulo Alberto Nogueira Figueiro/ Fernando Augusto Ramos Pontes/ Nelson Cruz Sampaio Neto/ Marcelle Pereira Mota','B1','0.5'),(15,'MARCELLE PEREIRA MOTA','Periodico','2017','Signifying Software Engineering to Computational Thinking Learners with AgentSheets and PoliFacets','10.1016/j.jvlc.2017.01.005','-','JOURNAL OF VISUAL LANGUAGES AND COMPUTING','MONTEIRO, INGRID TEIXEIRA/ DE CASTRO SALGADO, LUCIANA CARDOSO/ Marcelle Pereira Mota/ SAMPAIO, ANDR├ëIA LIB├ôRIO/ DE SOUZA, CLARISSE SIECKENIUS','-','SEM QUALIS'),(16,'MARCELLE PEREIRA MOTA','Periodico','2019','An Empirical Study on the Adaptation and Automation of a Cancellation Test for Children','10.5753/jis.2019.555','-','SBC JOURNAL ON 3D INTERACTIVE SYSTEMS','CASCAES, RENATA┬á/ LAMEIRA, KALILL┬á/ SARMANHO, RICARDO┬á/ SANTOS, SUZANE┬á/ PINHEIRO, KELLY┬á/ Marcelle Pereira Mota/ PEREIRA, ANT├öNIO┬á/ CRUZ SAMPAIO NETO, NELSON','-','SEM QUALIS');
/*!40000 ALTER TABLE `resultados` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-14 14:34:39

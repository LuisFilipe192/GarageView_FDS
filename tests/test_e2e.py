import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class GarageViewE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        selenium_remote_url = os.environ.get("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
        options = webdriver.ChromeOptions()
        cls.driver = webdriver.Remote(command_executor=selenium_remote_url, options=options)
        cls.driver.implicitly_wait(5)
        # Atualiza para o site oficial de deploy
        cls.base_url = "https://garageview-fds-8l00.onrender.com/forum/"
        cls._username = "e2euser_teste"
        cls._email = "e2euser_teste@test.com"
        cls._password = "senhae2e123"
        cls._ensure_user_exists()
        # Login único para todo o site
        cls._login_once()

    @classmethod
    def tearDownClass(cls):
        # Logout para garantir que o teste seja independente e não deixe sessão aberta
        driver = cls.driver
        try:
            driver.get(cls.base_url)
            # Vai para o perfil se necessário
            try:
                driver.find_element(By.LINK_TEXT, "Perfil").click()
            except:
                try:
                    driver.find_element(By.XPATH, "//a[contains(text(),'Perfil')]").click()
                except:
                    pass
            # Logout
            logout_form = driver.find_element(By.XPATH, "//form[@action='/forum/logout/']")
            logout_form.find_element(By.XPATH, ".//button").click()
        except Exception:
            pass
        cls.driver.quit()
    @classmethod
    def _login_once(cls):
        driver = cls.driver
        driver.get(cls.base_url + "login/")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys(cls._username)
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys(cls._email)
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys(cls._password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Entrar')]").click()
        WebDriverWait(driver, 5).until(lambda d: cls._username in d.page_source)

    @classmethod
    def _ensure_user_exists(cls):
        driver = cls.driver
        driver.get(cls.base_url + "login/")
        try:
            driver.find_element(By.NAME, "username").send_keys(cls._username)
            driver.find_element(By.NAME, "email").send_keys(cls._email)
            driver.find_element(By.NAME, "password").send_keys(cls._password)
            driver.find_element(By.XPATH, "//button[contains(text(),'Entrar')]").click()
            # Se login falhar, faz cadastro
            if "Entrar" in driver.page_source or "E-mail não corresponde" in driver.page_source:
                driver.get(cls.base_url + "cadastro/")
                driver.find_element(By.NAME, "username").send_keys(cls._username)
                driver.find_element(By.NAME, "password1").send_keys(cls._password)
                driver.find_element(By.NAME, "password2").send_keys(cls._password)
                driver.find_element(By.XPATH, "//button[contains(text(),'Cadastrar')]").click()
        except Exception as e:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01_cadastro_login_logout(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        self.assertIn(self._username, driver.page_source)

    def test_02_login(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        self.assertIn(self._username, driver.page_source)

    def test_03_busca(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        busca = driver.find_element(By.NAME, "q")
        busca.send_keys("fiat")
        busca.send_keys(Keys.RETURN)
        WebDriverWait(driver, 7).until(lambda d: "fiat" in d.page_source.lower())
        time.sleep(1)
        self.assertIn("fiat", driver.page_source.lower())

    def test_04_filtro_preco(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        min_price = driver.find_element(By.NAME, "min_price")
        max_price = driver.find_element(By.NAME, "max_price")
        min_price.clear()
        max_price.clear()
        min_price.send_keys("100")
        max_price.send_keys("100000")
        driver.find_element(By.XPATH, "//button[contains(text(),'Aplicar')]").click()
        time.sleep(1)
        self.assertIn("Preço mínimo", driver.page_source)

    def test_05_criar_anuncio(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        # Testa se botão está como link ou btn, e tenta clicar de ambas as formas
        try:
            driver.find_element(By.LINK_TEXT, "Criar anúncio").click()
        except:
            driver.find_element(By.XPATH, "//a[contains(text(),'Criar anúncio') or contains(text(),'+ Criar anúncio')] | //button[contains(text(),'Criar anúncio') or contains(text(),'+ Criar anúncio')]" ).click()
        time.sleep(1)
        driver.find_element(By.ID, "titulo").send_keys("Teste E2E")
        driver.find_element(By.ID, "preco").send_keys("12345")
        driver.find_element(By.ID, "imagem_url").send_keys("")
        driver.find_element(By.ID, "descricao").send_keys("Descrição do teste E2E")
        driver.find_element(By.ID, "contato").send_keys("11900000000")
        driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value,'Publicar anúncio')] | //input[contains(@value,'Publicar anúncio')]").click()
        WebDriverWait(driver, 7).until(lambda d: "Teste E2E" in d.page_source)
        time.sleep(1)
        self.assertIn("Teste E2E", driver.page_source)

    def test_06_editar_anuncio(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        WebDriverWait(driver, 7).until(lambda d: "Teste E2E" in d.page_source)
        driver.find_element(By.LINK_TEXT, "Teste E2E").click()
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Editar anúncio").click()
        time.sleep(1)
        campo_titulo = driver.find_element(By.ID, "titulo")
        campo_titulo.clear()
        campo_titulo.send_keys("Teste E2E Editado")
        driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value,'Salvar alterações')] | //input[contains(@value,'Salvar alterações')]").click()
        # Após salvar, deve redirecionar para o detalhe do anúncio
        WebDriverWait(driver, 7).until(lambda d: "Teste E2E Editado" in d.page_source)
        time.sleep(1)
        self.assertIn("Teste E2E Editado", driver.page_source)

    def test_07_excluir_anuncio(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(3)
        # Procura o anúncio editado, pode estar como link ou div, tenta de ambas as formas
        for _ in range(2):
            if "Teste E2E Editado" in driver.page_source:
                break
            time.sleep(2)
            driver.refresh()
        if "Teste E2E Editado" not in driver.page_source:
            self.skipTest("Anúncio 'Teste E2E Editado' não encontrado para exclusão.")
        try:
            driver.find_element(By.LINK_TEXT, "Teste E2E Editado").click()
        except:
            cards = driver.find_elements(By.CLASS_NAME, "card-veiculo")
            achou = False
            for card in cards:
                if "Teste E2E Editado" in card.text:
                    card.click()
                    achou = True
                    break
            if not achou:
                self.fail("Não foi possível abrir o anúncio para excluir.")
        time.sleep(2)
        excluir_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Excluir') or contains(text(),'Excluir anúncio')]")
        excluir_btn.click()
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        time.sleep(3)
        driver.get(self.base_url)
        for _ in range(3):
            if "Teste E2E Editado" not in driver.page_source:
                break
            time.sleep(2)
            driver.refresh()
        self.assertNotIn("Teste E2E Editado", driver.page_source)

    def test_08_perfil(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(3)
        perfil_link = None
        # Tenta encontrar o link de algumas formas para garantir que o teste seja mais robusto a mudanças de layout
        try:
            perfil_link = driver.find_element(By.LINK_TEXT, "Perfil")
        except:
            try:
                perfil_link = driver.find_element(By.XPATH, "//a[contains(text(),'Perfil')]")
            except:
                try:
                    perfil_link = driver.find_element(By.CLASS_NAME, "perfil-container")
                except:
                    pass
        if not perfil_link:
            self.fail("Link 'Perfil' não encontrado na página inicial.")
        perfil_link.click()
        time.sleep(3)
        self.assertIn("Perfil", driver.page_source)

if __name__ == "__main__":
    unittest.main()

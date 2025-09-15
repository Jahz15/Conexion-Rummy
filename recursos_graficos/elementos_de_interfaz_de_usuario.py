#IMPORTANTE 
##Querido colega programador:
##
##
## Cuando escribí este código, sólo Dios y yo
##
# sabíamos cómo funcionaba.
##
#Ahora, ¡sólo Dios lo sabe!
##
##
# Así que si está tratando de 'optimizarlo'
##
# y fracasa (seguramente), por favor,
##
# incremente el contador a continuación
##
# como una advertencia para su siguiente colega:
##
## total_horas_perdidas_aquí = 30


from recursos_graficos import constantes
import pygame

class Elemento_texto:
    def __init__(self, un_juego, texto, ancho, alto, x, y, tamaño_fuente, fuente, color, radio_borde=0, color_texto=(0, 0, 0), color_borde=(0, 0, 0), grosor_borde=0,alineacion="centro", alineacion_vertical=None,**kwargs):
        self.pantalla = un_juego.pantalla
        self.ancho, self.alto = ancho, alto
        self.x, self.y = x, y
        self.texto = texto
        self.tamaño_fuente = tamaño_fuente
        self.fuente = self.cargar_fuente(fuente)
        self.color = color
        self.color_actual = color
        self.color_texto = color_texto
        self.radio_borde = radio_borde
        self.color_borde = color_borde
        self.grosor_borde = grosor_borde
        self.color_borde_actual = self.color_borde
        self.alineacion = alineacion.lower()
        self.alineacion_vertical = alineacion_vertical
        
        #Atributos para el scrolleable
        self.scroll_offset = 0   # cuanto se ha desplazado hacia arriba/abajo
        self.scroll_activo = False
        self.scroll_rect = None  # rectángulo de la barra
        self.scroll_drag = False # si estoy arrastrando con el ratón


        # Crear rectángulo del elemento de texto
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.esta_hover = False
        self.visible = True
        
        # Preparar el texto
        self.prepar_texto()
    
    def cargar_fuente(self, fuente):
        try:
            return pygame.font.Font(fuente, self.tamaño_fuente)
        except FileNotFoundError:
            return pygame.font.SysFont(fuente, self.tamaño_fuente)
    
    def prepar_texto(self):
        """Divide el texto en líneas automáticamente si es muy largo"""
        # Calcular ancho máximo permitido (con margen) y guardar el ancho del texto renderizado
        ancho_maximo = self.ancho * 0.9
        ancho_texto = self.fuente.size(self.texto)[0]
        
        # Si el texto cabe en una línea, lo dejamos así
        if ancho_texto <= ancho_maximo:
            #la superficie de texto es el texto renderizado con el color
            self.superficie_texto = self.fuente.render(self.texto, True, self.color_texto)
            self.texto_una_linea()
            return
        
        # Si no cabe, preparamos texto con multiples lineas
        self.prepar_texto_multiple(ancho_maximo)
    # def prepar_scroll(self):
        
    def prepar_texto_multiple(self, ancho_maximo):
        # dividir por saltos de párrafo "\n"
        saltos_elementos = self.texto.split('\n')
        self.elementos_saltos = []

        # generar superficies para este bloque (puede ocupar varias líneas)
        for linea in saltos_elementos:
            #se guarda en superficies el arreglo con todas las superficies de el elemento
            superficies = self.texto_mutiple_maximo_espacio(linea, ancho_maximo) 
            self.elementos_saltos.append(superficies) #se agrega ese arreglo a otro [[],..]

        # posicionar cada bloque de superficies
        self.rects_texto = []
        self.ajustar_posicion_elementos()


    def texto_mutiple_maximo_espacio(self, linea, ancho_maximo):
        #Definimos lineas que guarda cada linea nececesaria para dividir la "linea" de parametro, en varias
        lineas = []
        linea_actual = ""
        palabras = linea.split(' ')

        for palabra in palabras:
            #Prueba concatena si es que linea actual ya tiene una palabra
            prueba = f"{linea_actual} {palabra}".strip() if linea_actual else palabra
            
            #tamño del ancho del texto que tenga palabra ya renderizado
            ancho_texto_prueba = self.fuente.size(prueba)[0] 
            
            #actualiza la linea actual si es que se puede, sino simplemente termina la linea y solo la agrega a lineas
            if ancho_texto_prueba <= ancho_maximo:
                linea_actual = prueba 
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra #-> se reinicia linea_actual con la palabra que no se pudo agregar

        #Permite agregar la ultima linea
        if linea_actual:
            lineas.append(linea_actual)

        #Se recorre lineas, cada linea si renderiza y si agrega a superficie, es decir es exactamente el arreglo pero cada elemento ya esta renderizado
        superficies = []
        for linea in lineas:
            superficie = self.fuente.render(linea, True, self.color_texto)
            superficies.append(superficie)

        return superficies  # devolver el conjunto de lineas renderizadas


    def ajustar_posicion_elementos(self):
        """Posicionar cada bloque de líneas (separados por '\n')."""

        y_actual = self.rect.top + self.alto * 0.02  # margen arriba
        espacio_dejar_x = self.ancho * 0.02
        self.rects_texto = []
        self.superficies_texto_planas = []

        #Recorre el elementos_saltos, cada bloque es un arreglo (que tiene todos los textos renderizados de ese bloque)
        for bloque in self.elementos_saltos:
            #guardamos en rects_bloque el arreglo con las posiciones
            rects_bloque = self.ajustar_posicion_lineas(bloque, y_actual, espacio_dejar_x)
            
            #Agregas elementos a las listas correspondientes
            self.rects_texto.extend(rects_bloque)
            self.superficies_texto_planas.extend(bloque)  

            #se suma el valor del altro de cada superficie del bloque, y se le suma la longitud del (bloque-1)*5
            alto_bloque = sum(superficie.get_height() for superficie in bloque) + (len(bloque)-1)*5
            y_actual += alto_bloque + 20

        # altura total de todo el texto
        alto_total = self.rects_texto[-1].bottom - self.rects_texto[0].top  

        # activar scroll si sobrepasa
        if alto_total > self.alto:
            self.scroll_activo = True
            # calcular altura de la barra proporcional
            visible_ratio = self.alto / alto_total
            barra_altura = max(20, self.alto * visible_ratio)
            self.scroll_rect = pygame.Rect(
                self.rect.right - self.ancho*0.05,  # pegada al borde derecho
                self.rect.top,
                self.ancho*0.01,  # ancho barra
                barra_altura
            )
        else:
            self.scroll_activo = False
            self.scroll_rect = None




    def ajustar_posicion_lineas(self, bloque, y_inicial, espacio_dejar_x):
        rects_texto = []
        y = y_inicial

        #recorremos bloque(lista de superficies)
        for superficie in bloque:
            ancho_linea = superficie.get_width()

            if self.alineacion == "izquierda":
                x = self.rect.left + espacio_dejar_x
            elif self.alineacion == "derecha":
                x = self.rect.right - ancho_linea - espacio_dejar_x
            else:  # centro
                x = self.rect.centerx - ancho_linea / 2

            rects_texto.append(pygame.Rect(x, y, ancho_linea, superficie.get_height()))
            y += superficie.get_height() + 5  # 5px entre líneas del mismo bloque
        
        return rects_texto

    
    def texto_una_linea(self):
        """Posiciona texto de una sola línea, dependiendo de la alineacion y la alineacion_vertical, usamos .right por ejemplo para saber la ubicacion del borde derecho sin tenerr que calcular nada"""
        espacio_dejar_x = self.ancho*0.02
        espacio_dejar_y = self.alto*0.02
        match self.alineacion:
            case "izquierda":  x_pos = self.rect.left + espacio_dejar_x
            case "derecha": x_pos = self.rect.right - espacio_dejar_x
            case _: x_pos = self.rect.centerx
        match self.alineacion_vertical:
            case "arriba": y_pos = self.rect.top + espacio_dejar_y
            case "abajo": y_pos = self.rect.bottom - espacio_dejar_y
            case _: y_pos = self.rect.centery
        
        #Determina la ubicacion, los "midleft" posicionan desde la izquierda en el eje x, es decir miden desde la izquierda del eje horizontal, y centran el "centro del elemento a ubicar" en una linea imaginaria y que tambien representa una posicion, y mide desde arriba.
        if self.alineacion == "izquierda":
            self.rect_texto = self.superficie_texto.get_rect(midleft=(x_pos, y_pos))
        elif self.alineacion == "derecha":
            self.rect_texto = self.superficie_texto.get_rect(midright=(x_pos, y_pos))
        else:
            self.rect_texto = self.superficie_texto.get_rect(center=(x_pos, y_pos))

    def dibujar(self):
        if self.visible:
            # Dibujar fondo y borde
            pygame.draw.rect(self.pantalla, self.color_actual, self.rect, border_radius=self.radio_borde)
            if self.grosor_borde > 0:
                pygame.draw.rect(self.pantalla, self.color_borde_actual, self.rect, 
                                self.grosor_borde, border_radius=self.radio_borde)
            
            # Dibujar texto
            if hasattr(self, 'superficies_texto_planas'):
                for superficie, rect in zip(self.superficies_texto_planas, self.rects_texto):
                    rect_scroll = rect.move(0, -self.scroll_offset)  # aplicar offset
                    if rect_scroll.colliderect(self.rect):  # pintar solo si está dentro del área
                        self.pantalla.blit(superficie, rect_scroll)
            else:
                rect_scroll = self.rect_texto.move(0, -self.scroll_offset)
                if rect_scroll.colliderect(self.rect):
                    self.pantalla.blit(self.superficie_texto, rect_scroll)

            # dibujar scroll si corresponde
            if self.scroll_activo and self.scroll_rect:
                pygame.draw.rect(self.pantalla, (100,100,100), self.scroll_rect)


    
    def mostrar(self): self.visible = True
    def ocultar(self): self.visible = False
    def verificar_hover(self, posicion_raton): pass
    def max_scroll(self):
        return (self.rects_texto[-1].bottom - self.rects_texto[0].top) - self.alto
    def sync_barra(self):
        """Sincroniza la posición de la barra según el scroll_offset actual."""
        if not self.scroll_activo or not self.scroll_rect:
            return
        ratio = self.scroll_offset / self.max_scroll() if self.max_scroll() > 0 else 0
        self.scroll_rect.top = self.rect.top + ratio * (self.rect.height - self.scroll_rect.height)

    def manejar_evento(self, evento):
        if not self.visible:  # Solo procesar eventos si es visible
            return False
        if not self.scroll_activo:
            return

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:  # rueda arriba
                self.scroll_offset = max(0, self.scroll_offset - 20)
                self.sync_barra()
            elif evento.button == 5:  # rueda abajo
                self.scroll_offset = min(
                    self.max_scroll(),
                    self.scroll_offset + 20
                )
                self.sync_barra()
            elif self.scroll_rect and self.scroll_rect.collidepoint(evento.pos):
                self.scroll_drag = True
                self.drag_y = evento.pos[1] - self.scroll_rect.top

        elif evento.type == pygame.MOUSEBUTTONUP:
            self.scroll_drag = False

        elif evento.type == pygame.MOUSEMOTION and self.scroll_drag:
            # mover barra con el ratón
            nueva_top = evento.pos[1] - self.drag_y
            nueva_top = max(self.rect.top, min(nueva_top, self.rect.bottom - self.scroll_rect.height))
            self.scroll_rect.top = nueva_top

            # convertir posición barra -> scroll_offset
            ratio = (self.scroll_rect.top - self.rect.top) / (self.rect.height - self.scroll_rect.height)
            self.scroll_offset = ratio * self.max_scroll()



class Boton(Elemento_texto):
    def __init__(self, *args, color_hover=None, color_borde_hover=None, 
                 color_borde_clicado=None, accion=None, **kwargs):
        
        # Pasar todos los argumentos posicionales y nombrados al padre
        super().__init__(*args, **kwargs)
        
        # Atributos específicos de Boton
        self.color_hover = color_hover
        self.color_borde_hover = color_borde_hover
        self.color_borde_clicado = color_borde_clicado
        self.accion = accion
        self.presionado = False

    def verificar_hover(self, posicion_raton):
        estaba_hover = self.esta_hover
        self.esta_hover = self.rect.collidepoint(posicion_raton) 
        
        if self.esta_hover != estaba_hover:
            if self.esta_hover and self.color_borde_hover:
                self.color_borde_actual = self.color_borde_hover
            elif not self.esta_hover:
                self.color_borde_actual = self.color_borde
            return True
        return False

    def manejar_evento(self, evento):
        if not self.visible:
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.esta_hover:
                if self.color_borde_clicado:
                    self.color_borde_actual = self.color_borde_clicado
                self.presionado = True
                return True

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.presionado and self.esta_hover:
                if self.accion:
                    self.accion()
            self.presionado = False
            return True

        return False



"""En caso de ser un boton tipo radio"""
class BotonRadio(Boton):
    def __init__(self, *args, grupo=None,valor=None, deshabilitado=False, **kwargs):
        self.deshabilitado = deshabilitado
        self.seleccionado = False
        self.grupo = grupo
        self.valor = valor
        super().__init__(*args, **kwargs)
        self.deshabilitar()
    def verificar_hover(self, posicion_raton):
        if self.deshabilitado:
            return False
        """Sobrescribe el método de Boton para que el borde no cambie si está seleccionado"""
        estaba_hover = self.esta_hover
        self.esta_hover = self.rect.collidepoint(posicion_raton)

        if self.esta_hover != estaba_hover:
            if not self.seleccionado:  # Solo cambiar el borde si NO está seleccionado
                self.color_borde_actual = self.color_borde_hover if self.esta_hover else self.color_borde
            return True
    def sobre_el_elemento(self, con_retorno, funcion=None):
        if self.esta_hover and not self.seleccionado:
            if self.grupo:
                for boton in self.grupo:
                    boton.deseleccionar()
            self.seleccionar()
            if self.accion:
                self.accion(self)
            if con_retorno:
                return True
            if funcion is not None:
                funcion()
        return False

    def manejar_evento(self, evento):
        if not self.visible or self.deshabilitado:
            return False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if hasattr(evento, 'pos') and self.rect.collidepoint(evento.pos):
                # seleccionar y ejecutar acción
                self.sobre_el_elemento(True)
                return True
        return False


    def seleccionar(self):
        self.seleccionado = True
        self.color_borde_actual = self.color_borde_clicado

    def deseleccionar(self):
        self.seleccionado = False
        self.color_borde_actual = self.color_borde
        self.deshabilitar()
    def deshabilitar(self):
        if self.deshabilitado:
            self.color_borde_actual = (100, 100, 100)  # Gris para deshabilitado
            self.color_texto = (100, 100, 100)
class EntradaTexto(BotonRadio):
    def __init__(self, *args, valor="", limite_caracteres=None, grupo=None, permitir_espacios=False, permitir_numeros=False, permitir_especiales=False, cartel_alerta= None, **kwargs):
        self.permitir_espacios = permitir_espacios
        self.permitir_numeros = permitir_numeros
        self.permitir_especiales = permitir_especiales
        self.texto_valido = True
        self.cartel_alerta = cartel_alerta
        super().__init__(*args, grupo=grupo, valor=None, **kwargs)
        self.valor = valor
        self.limite_caracteres = limite_caracteres
        self.pos_cursor = len(valor)
        self.mostrar_cursor = True
        self.ultima_tecla = None
        self.tiempo_repeticion = 30
        self.retardo_inicial = 200
        self.ultimo_borrado = 0
        self.ultimo_parpadeo = pygame.time.get_ticks()

        self.actualizar_texto()
    def mover_cursor(self,evento):
        click_x = evento.pos[0]
        x_texto_inicial = self.rect_texto.x
        self.pos_cursor = len(self.valor)
        for i in range(len(self.valor) + 1):
            ancho_parcial = self.fuente.render(self.valor[:i], True, self.color_texto).get_width()
            if x_texto_inicial + ancho_parcial >= click_x:
                self.pos_cursor = i
                break
    def procesar_tecla(self,evento):
        if self.seleccionado and evento.type == pygame.KEYDOWN:
            self.ultima_tecla = evento.key
            self.mostrar_cursor = True
            self.ultimo_parpadeo = pygame.time.get_ticks()

            if evento.key == pygame.K_BACKSPACE:
                self.ultimo_borrado = pygame.time.get_ticks()
                if self.pos_cursor > 0:
                    self.valor = self.valor[:self.pos_cursor-1] + self.valor[self.pos_cursor:]
                    self.pos_cursor -= 1
            elif evento.key == pygame.K_RETURN:
                self.deseleccionar()
            elif evento.key == pygame.K_LEFT and self.pos_cursor > 0:
                self.pos_cursor -= 1
            elif evento.key == pygame.K_RIGHT and self.pos_cursor < len(self.valor):
                self.pos_cursor += 1
            elif evento.key == pygame.K_SPACE and not self.permitir_espacios:
                # No permitir espacios
                return True
            else:
                if (not self.limite_caracteres or len(self.valor) < self.limite_caracteres) and evento.unicode:
                    # Validar el carácter antes de agregarlo
                    if not self.validar_caracter(evento.unicode):
                        return True  # No agregar el carácter, ya se mostró el cartel
                    self.valor = self.valor[:self.pos_cursor] + evento.unicode + self.valor[self.pos_cursor:]
                    self.pos_cursor += 1
                    self.validar_texto()

            self.actualizar_texto()
            return True

    def mostrar_alerta(self, mensaje):
        """Muestra un mensaje de alerta en el cartel"""
        if self.cartel_alerta:
            # Posicionar el cartel cerca del campo de entrada
            cartel_x = self.rect.x
            cartel_y = self.rect.y - 110  # Sobre el campo de entrada
            self.cartel_alerta.x = cartel_x
            self.cartel_alerta.y = cartel_y
            self.cartel_alerta.rect = pygame.Rect(cartel_x, cartel_y, 
                                                self.cartel_alerta.ancho, 
                                                self.cartel_alerta.alto)
            self.cartel_alerta.boton_cerrar_rect = pygame.Rect(
                cartel_x + self.cartel_alerta.ancho - 30, 
                cartel_y + 10, 20, 20
            )
            self.cartel_alerta.mostrar(mensaje)
        
        # También cambiar color del borde para feedback visual
        self.color_borde_actual = (255, 0, 0)
        
    def validar_caracter(self, caracter):
        """Valida si un carácter es permitido"""
            # No permitir espacios
        if caracter.isspace() and not self.permitir_espacios:
            self.mostrar_alerta("¡Nombre no válido! Recuerda no utilizar números o caracteres especiales.")
            return False
            
            # No permitir números
        if caracter.isdigit() and not self.permitir_numeros:
            self.mostrar_alerta("¡Nombre no válido! Recuerda no utilizar números o caracteres especiales.")
            return False
            
            # Permitir letras y caracteres especiales básicos
        if not self.permitir_especiales and not caracter.isalpha():
            self.mostrar_alerta("¡Nombre no válido! Recuerda no utilizar números o caracteres especiales.")
            return False
        return caracter.isprintable()
        
        
    def validar_texto(self):
        texto = self.valor.strip()

        if len(texto) > self.limite_caracteres:
            self.texto_valido = False
            self.color_borde_actual = (255, 0, 0)
            return

        if len(texto) == 0:
            self.texto_valido = False
            self.color_borde_actual = (255, 0, 0)
            return
        
        if not self.permitir_espacios and ' ' in texto:
            self.texto_valido = False
            self.color_borde_actual = (255, 0, 0)
            return

        if not self.permitir_numeros and any(caracter.isdigit() for caracter in texto):
            self.texto_valido = False
            self.color_borde_actual = (255, 0, 0)
            return

        self.texto_valido = True
        self.color_borde_actual = self.color_borde
        return True
    
    def obtener_texto_validado(self):
        """Retorna el texto validado y limpio"""
        texto = self.valor.strip()
        if not self.permitir_espacios:
            texto = texto.replace(' ', '')
        if not self.permitir_numeros:
            texto = ''.join(c for c in texto if not c.isdigit())
        return texto
    
    def manejar_evento(self, evento):
        if not self.visible:
            return False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if hasattr(evento, 'pos') and self.rect.collidepoint(evento.pos):
                self.sobre_el_elemento(False, lambda: self.mover_cursor(evento))
                return True
        self.procesar_tecla(evento)
        if self.seleccionado and evento.type == pygame.KEYUP:
            if evento.key == pygame.K_BACKSPACE:
                self.ultima_tecla = None
                self.ultimo_borrado = 0
            else:
                self.ultima_tecla = None

        return False

    def actualizar(self):
        ahora = pygame.time.get_ticks()

        if self.seleccionado and self.ultima_tecla == pygame.K_BACKSPACE:
            if self.ultimo_borrado != 0 and ahora - self.ultimo_borrado > self.retardo_inicial:
                if (ahora - self.ultimo_borrado) % self.tiempo_repeticion < 20:
                    if self.pos_cursor > 0:
                        self.valor = self.valor[:self.pos_cursor-1] + self.valor[self.pos_cursor:]
                        self.pos_cursor -= 1
                        self.actualizar_texto()
                    self.mostrar_cursor = True
                    self.ultimo_parpadeo = ahora
        elif ahora - self.ultimo_parpadeo > 500:
            self.mostrar_cursor = not self.mostrar_cursor
            self.ultimo_parpadeo = ahora

    def actualizar_texto(self):
        self.texto = self.valor
        self.prepar_texto()
        self.validar_texto()

        # Cambiar color del borde según validación
        if not self.texto_valido:
            self.color_borde_actual = (255, 0, 0)  # Rojo para error
        else:
            self.color_borde_actual = self.color_borde  # Color normal

    def dibujar(self):
        self.actualizar()
        super().dibujar()
        if self.seleccionado and self.mostrar_cursor:
            if self.valor:  # Solo si hay texto
                ancho_texto_parcial = self.fuente.render(self.valor[:self.pos_cursor], True, self.color_texto).get_width()
            else:
                ancho_texto_parcial = 0  # No hay nada escrito
            
            x_texto_inicial = self.rect_texto.x
            x_cursor = x_texto_inicial + ancho_texto_parcial
            y_inicio = self.rect.y + 5
            y_fin = self.rect.y + self.rect.height - 5
            pygame.draw.line(self.pantalla, self.color_texto, (x_cursor, y_inicio), (x_cursor, y_fin), 2)
    def verificar_hover(self, posicion_raton):
        return super().verificar_hover(posicion_raton)
class CartelAlerta:
    def __init__(self, pantalla, mensaje, x, y, ancho=500, alto=300):
            self.pantalla = pantalla
            self.mensaje = mensaje
            self.ancho = ancho
            self.alto = alto
            self.x = x
            self.y = y
            self.visible = False
            self.rect = pygame.Rect(x, y, ancho, alto)
            
            # Colores
            self.color_fondo = constantes.ELEMENTO_FONDO_PRINCIPAL
            self.color_borde = constantes.ELEMENTO_BORDE_CUATERNARIO
            self.color_texto = constantes.COLOR_TEXTO_PRINCIPAL
            self.radio_borde = constantes.REDONDEO_NORMAL
            self.grosor_borde = constantes.BORDE_PRONUNCIADO
            
            # Botón de cerrar
            self.boton_cerrar_rect = pygame.Rect(x + ancho - 30, y + 10, 20, 20)
            
            # Preparar texto
            self.fuente = pygame.font.SysFont(constantes.FUENTE_LLAMATIVA, 50)
            self.preparar_texto()
        
    def preparar_texto(self):
            """Divide el mensaje en líneas si es muy largo"""
            palabras = self.mensaje.split(' ')
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                prueba = f"{linea_actual} {palabra}".strip() if linea_actual else palabra
                ancho_prueba = self.fuente.size(prueba)[0]
                
                if ancho_prueba <= self.ancho - 20:  # Margen de 20px
                    linea_actual = prueba
                else:
                    if linea_actual:
                        lineas.append(linea_actual)
                    linea_actual = palabra
            
            if linea_actual:
                lineas.append(linea_actual)
            
            self.lineas = lineas

    def centrar_en_pantalla(self):
        ancho_pantalla = self.pantalla.get_width()
        alto_pantalla = self.pantalla.get_height()
        self.x = (ancho_pantalla - self.ancho) // 2
        self.y = (alto_pantalla - self.alto) // 2
        self.rect.topleft = (self.x, self.y)
        self.boton_cerrar_rect.topleft = (self.x + self.ancho - 30, self.y + 10)
        
    def mostrar(self, mensaje=None):
            """Muestra el cartel con un mensaje opcional"""
            if mensaje:
                self.mensaje = mensaje
                self.preparar_texto()
            self.centrar_en_pantalla()
            self.visible = True
        
    def ocultar(self):
            """Oculta el cartel"""
            self.visible = False
        
    def manejar_evento(self, evento):
            """Maneja eventos del ratón para cerrar el cartel"""
            if not self.visible:
                return False
                
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.boton_cerrar_rect.collidepoint(evento.pos):
                    self.ocultar()
                    return True
                    
            return False
        
    def verificar_hover(self, posicion_raton):
            """Verifica hover sobre el botón de cerrar"""
            if not self.visible:
                return False
            return self.boton_cerrar_rect.collidepoint(posicion_raton)
        
    def dibujar(self):
            """Dibuja el cartel de alerta"""
            if not self.visible:
                return
                
            # Dibujar fondo y borde
            pygame.draw.rect(self.pantalla, self.color_fondo, self.rect, border_radius=self.radio_borde)
            pygame.draw.rect(self.pantalla, self.color_borde, self.rect, self.grosor_borde, border_radius=self.radio_borde)
            
            # Dibujar botón de cerrar (X)
            pygame.draw.rect(self.pantalla, (255, 100, 100), self.boton_cerrar_rect, border_radius=5)
            pygame.draw.line(self.pantalla, (255, 255, 255), 
                            (self.boton_cerrar_rect.left + 5, self.boton_cerrar_rect.top + 5),
                            (self.boton_cerrar_rect.right - 5, self.boton_cerrar_rect.bottom - 5), 2)
            pygame.draw.line(self.pantalla, (255, 255, 255),
                            (self.boton_cerrar_rect.right - 5, self.boton_cerrar_rect.top + 5),
                            (self.boton_cerrar_rect.left + 5, self.boton_cerrar_rect.bottom - 5), 2)
            
            # --- CENTRAR EL TEXTO ---
            # Calcular altura total del bloque de texto
            total_text_height = 0
            text_surfaces = []
            for linea in self.lineas:
                surface = self.fuente.render(linea, True, self.color_texto)
                text_surfaces.append(surface)
                total_text_height += surface.get_height()
            total_text_height += 5 * (len(self.lineas) - 1)  # Espacio entre líneas

            # Coordenada Y inicial para centrar verticalmente
            y_texto = self.rect.y + (self.alto - total_text_height) // 2

            # Dibujar cada línea centrada horizontalmente
            for surface in text_surfaces:
                x_texto = self.rect.x + (self.ancho - surface.get_width()) // 2
                self.pantalla.blit(surface, (x_texto, y_texto))
                y_texto += surface.get_height() + 5
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



import pygame

class Elemento_texto:
    def __init__(self, un_juego, texto, ancho, alto, x, y, tamaño_fuente, fuente, color, radio_borde=0, color_texto=(0, 0, 0), color_borde=(0, 0, 0), grosor_borde=0,alineacion="centro", alineacion_vertical=None):
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
    def __init__(self, *args, grupo=None,valor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.seleccionado = False
        self.grupo = grupo
        self.valor = valor
    def verificar_hover(self, posicion_raton):
        """Sobrescribe el método de Boton para que el borde no cambie si está seleccionado"""
        estaba_hover = self.esta_hover
        self.esta_hover = self.rect.collidepoint(posicion_raton)

        if self.esta_hover != estaba_hover:
            if not self.seleccionado:  # Solo cambiar el borde si NO está seleccionado
                self.color_borde_actual = self.color_borde_hover if self.esta_hover else self.color_borde
            return True
    def sobre_el_elemento(self, con_retorno, funcion=None):
        if self.esta_hover:
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
        if not self.visible:
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
class EntradaTexto(BotonRadio):
    def __init__(self, *args, valor="", limite_caracteres=None, grupo=None, **kwargs):
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
            else:
                if (not self.limite_caracteres or len(self.valor) < self.limite_caracteres) and evento.unicode:
                    self.valor = self.valor[:self.pos_cursor] + evento.unicode + self.valor[self.pos_cursor:]
                    self.pos_cursor += 1

            self.actualizar_texto()
            return True
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

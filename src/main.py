import flet as ft
from time import sleep

lista_de_colores = [
    ft.Colors.LIGHT_BLUE,
    ft.Colors.PURPLE,
    ft.Colors.TEAL,
    ft.Colors.ORANGE,
    ft.Colors.DEEP_PURPLE,
    ft.Colors.INDIGO,
    ft.Colors.BLUE,
    ft.Colors.CYAN,
    ft.Colors.GREEN,
    ft.Colors.LIGHT_GREEN,
    ft.Colors.LIME,
    ft.Colors.YELLOW,
    ft.Colors.AMBER,
    ft.Colors.DEEP_ORANGE,
    ft.Colors.BROWN,
    ft.Colors.GREY,
    ft.Colors.BLUE_GREY,
    ft.Colors.WHITE,
    ft.Colors.PINK,
    ft.Colors.RED,
]

def obtener_color():
    index = 0
    while True:
        yield lista_de_colores[index]
        index = (index + 1) % len(lista_de_colores)  # Reiniciar la lista al llegar al final

# Crear un generador de colores
generador_de_colores = obtener_color()

def siguiente_color():
    return next(generador_de_colores)

def main(page: ft.Page):
    #Configuraciones de ventana
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.always_on_bottom = False
    page.window.always_on_top = False
    page.window.frameless = False #Si la ventana de la aplicación debe no tener marco.
    page.window.full_screen = False
    page.window.ignore_mouse_events = False
    page.window.resizable = True #Si se puede cambiar el tamaño de la ventana de la aplicación.
    page.window.title_bar_hidden = True #Ocultar barra de arriba
    page.window.title_bar_buttons_hidden = True #Ocultar barra de arriba
    page.window.shadow = True
    page.padding = 0
    page.window.maximized = True

    # Lista para almacenar los procesos
    procesos = []
    lista_de_progress_bar = ft.Column([],spacing=0)
    regla = ft.Row([],width=950,height=20,spacing=0,wrap=False,vertical_alignment=ft.CrossAxisAlignment.START,alignment=ft.MainAxisAlignment.CENTER)
    texto_ejecucion_de_proceso = ft.Text("EJECUCIÓN DE PROCESOS", color="#000000", weight="bold", size=20,visible=False)

    # Controles de entrada
    nombre_proceso = ft.TextField(label="Nombre del Proceso",fill_color="#2d40a5",border_color="white")
    rafaga_cpu = ft.TextField(label="Ráfaga CPU", fill_color="#2d40a5",border_color="white",input_filter=ft.NumbersOnlyInputFilter())
    tiempo_llegada = ft.TextField(label="Tiempo de Llegada", fill_color="#2d40a5",border_color="white",input_filter=ft.NumbersOnlyInputFilter())

    # Tabla para mostrar los procesos ingresados
    tabla_procesos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Proceso")),
            ft.DataColumn(ft.Text("Ráfaga CPU")),
            ft.DataColumn(ft.Text("T. Llegada")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[],
        bgcolor="#197dba",
        border=ft.border.all(2, "black"),
        horizontal_lines = ft.BorderSide(1, "black"),
    )

    # Tabla para mostrar los resultados
    tabla_resultados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Proceso", color="#000000")),
            ft.DataColumn(ft.Text("T. Espera", color="#000000")),
            ft.DataColumn(ft.Text("T. Retorno", color="#000000")),
            ft.DataColumn(ft.Text("Estado", color="#000000")),
        ],
        rows=[],
        bgcolor="#ffffff",
        border=ft.border.all(2, "black"),
        horizontal_lines = ft.BorderSide(1, "black"),
    )

    # Función para agregar un proceso
    def agregar_proceso(e):
        procesos.append({
            "nombre": nombre_proceso.value,
            "rafaga": int(rafaga_cpu.value),
            "llegada": int(tiempo_llegada.value),
            "estado": "Dispuesto"
        })
        tabla_procesos.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(nombre_proceso.value)),
                    ft.DataCell(ft.Text(rafaga_cpu.value)),
                    ft.DataCell(ft.Text(tiempo_llegada.value)),
                    ft.DataCell(ft.Text("Dispuesto")),
                ]
            )
        )
        nombre_proceso.value = ""
        rafaga_cpu.value = ""
        tiempo_llegada.value = ""
        
        page.update()

    # Función para iniciar la simulación FIFO
    def iniciar_fifo(e):
        if len(tabla_procesos.rows) > 0:
            print("si hay")
        else:
            return
        nonlocal texto_ejecucion_de_proceso
        texto_ejecucion_de_proceso.visible = True
        texto_ejecucion_de_proceso.update()
        tabla_resultados.rows = None
        label_tiempo_medio_espera.value = ""
        label_tiempo_medio_retorno.value = ""

        # Ordenar procesos por tiempo de llegada
        procesos.sort(key=lambda x: x["llegada"])

        tiempo_actual = 0
        resultados = []
        tiempo_retorno = 0
        for proceso in procesos:
            if tiempo_actual < proceso["llegada"]:
                tiempo_actual = proceso["llegada"]
            tiempo_espera = tiempo_actual - proceso["llegada"]
            tiempo_retorno = tiempo_retorno + proceso["rafaga"]
            resultados.append({
                "nombre": proceso["nombre"],
                "espera": tiempo_espera,
                "retorno": tiempo_retorno,
                "estado": "Procesado",
                "rafaga": proceso["rafaga"]
            })
            tiempo_actual += proceso["rafaga"]

        # Calcular promedios   dividiendo la suma de los tiempos de espera y retorno entre el número de procesos
        tiempo_medio_espera = sum(r["espera"] for r in resultados) / len(resultados)
        tiempo_medio_retorno = sum(r["retorno"] for r in resultados) / len(resultados)
        
        # Número de segmentos REGLA
        numero_de_segmentos = tiempo_actual
        segmento_ancho = 950 / numero_de_segmentos

        for i in range(numero_de_segmentos):
            # Crear un contenedor para cada segmento
            segment = ft.Container(
                width=segmento_ancho,
                height=20,
                border=ft.border.only(right=ft.border.BorderSide(1, "white")) if i < numero_de_segmentos - 1 else None,
                alignment=ft.alignment.center,
                content=ft.Text(value=str(i+1), size=15),  # Mostrar el número
                bgcolor="#30419b"
            )
            regla.controls.append(segment)
        regla.update()

        anterior = 0
        # Mostrar resultados en la tabla
        for resultado in resultados:

            porcentaje_1 = (resultado["rafaga"]/tiempo_actual)*100
            porcentaje_real = (porcentaje_1 / 100) * 950 
            color_actual = siguiente_color()
            lista_de_progress_bar.controls.append(
                ft.Row([ft.Container(width=anterior),pb := ft.ProgressBar(width=porcentaje_real,height=50,color=color_actual,bgcolor="white")],spacing=0)
            )
            anterior = anterior + porcentaje_real
            #tiempo total
            tiempo_total = resultado["rafaga"]  #seg
            pasos = 100
            #incremento por paso
            incremento = 1 / pasos
            #tiempo de espera por paso
            tiempo_por_paso = tiempo_total / pasos

            for i in range(pasos + 1):
                pb.value = i * incremento
                sleep(tiempo_por_paso)
                page.update()

            tabla_resultados.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(resultado["nombre"],weight="bold", color="#ffffff")),
                        ft.DataCell(ft.Text(str(resultado["espera"]), color="#ffffff")),
                        ft.DataCell(ft.Text(str(resultado["retorno"]), color="#ffffff")),
                        ft.DataCell(ft.Text(resultado["estado"],color="#ffffff")),
                    ],
                    color=color_actual
                )
            )
            tabla_resultados.update()

        label_tiempo_medio_espera.value = f"{tiempo_medio_espera:.2f} ut"
        label_tiempo_medio_retorno.value = f"{tiempo_medio_retorno:.2f} ut"
        tabla_medios.visible = True
        page.update()




    def eliminar_simulacion(e):
        nonlocal procesos
        procesos = []
        lista_de_progress_bar.controls = []
        regla.controls = []
        tabla_resultados.rows = None
        label_tiempo_medio_espera.value = ""
        label_tiempo_medio_retorno.value = ""
        tabla_procesos.rows = None
        tabla_medios.visible = False
        texto_ejecucion_de_proceso.visible = False
        page.update()

    contenedor_ingresos = ft.Container(
        content=ft.Column([
            ft.Text("FIRST IN FIRST OUT",size=31,font_family="Bauhaus 93"),
            ft.Divider(color="white",trailing_indent=200, leading_indent=0),
            ft.Container(height=40),
            ft.ElevatedButton("Iniciar Simulación",icon=ft.Icons.SMART_DISPLAY_SHARP, bgcolor="#239b56",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "#f1c40f",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,},
                color={ft.ControlState.HOVERED: "#f1c40f",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,},
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, "#239b56"),
                    ft.ControlState.HOVERED: ft.BorderSide(2, "#f1c40f"),
                },
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                },
                alignment=ft.alignment.center_left
            ), height=40, width=260, on_click=iniciar_fifo),
            ft.Container(height=40),
            ft.Divider(color="white",trailing_indent=200, leading_indent=0),
            ft.Container(height=10),
            #===============================================================================================
            #Botones abajo de ANÁLISIS
            ft.Text("INGRESE DATOS DE UN PROCESO:", weight="bold"),
            ft.Container(height=20),
            nombre_proceso,
            ft.Container(height=20),
            rafaga_cpu,
            ft.Container(height=20),
            tiempo_llegada,
            ft.Container(height=20),
            ft.Divider(color="white",trailing_indent=200, leading_indent=0),
            ft.Container(height=20),      
            ft.ElevatedButton("Agregar proceso",icon=ft.Icons.ADD, bgcolor="#197dba",color="white",icon_color="white",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), height=40, width=260,on_click=agregar_proceso
            ),
            ft.Container(height=20), 
            ft.ElevatedButton("Eliminar simulación",icon=ft.Icons.DELETE, bgcolor="red",color="white",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color="white",
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), height=40, width=260,on_click=eliminar_simulacion
            ),
            ft.Container(height=50),

            ft.Container(content=ft.Row([ft.Icon(ft.Icons.COPYRIGHT,size=18),ft.Text("Escuela de Informática-UNT",font_family="Consolas")]),expand=True,alignment=ft.alignment.bottom_center,padding=10)
        ],spacing=0),
        bgcolor="#30419b", width=300,margin=0, padding=ft.Padding(left=20,right=20,top=10,bottom=0)
    )

    label_tiempo_medio_espera = ft.Text("",weight="bold", color="#000000")
    label_tiempo_medio_retorno = ft.Text("",weight="bold", color="#000000")

    tabla_medios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tiempo Medio de Espera:",weight="bold", color="#000000")),
            ft.DataColumn(label_tiempo_medio_espera),
            ft.DataColumn(ft.Text("Tiempo Medio de Retorno:",weight="bold", color="#000000")),
            ft.DataColumn(label_tiempo_medio_retorno),
        ],
        bgcolor="#ffffff",
        border=ft.border.only(bottom=ft.border.BorderSide(2, "black"),left=ft.border.BorderSide(2, "black"),right=ft.border.BorderSide(2, "black"),top=ft.border.BorderSide(2, "black")),
        horizontal_lines = ft.BorderSide(1, "black"), visible=False, width=536
    )

    def minimizar(e):
        page.window.minimized = True
        page.update()
    
    def maximizar(e):
        page.window.maximized = True
        page.update()

    page.add(
        ft.Row([
            contenedor_ingresos,
            ft.Column([
                ft.Row([
                    ft.WindowDragArea(ft.Container(
                        content=ft.Row([ft.Image(src="icon.png", height=30), ft.Text("Simulación", font_family="Harlow Solid", weight="bold", color="#000000", size=30)]),
                        bgcolor=ft.Colors.WHITE, padding=10
                    ), expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.IconButton(
                                ft.Icons.ARROW_CIRCLE_DOWN_OUTLINED,
                                on_click=minimizar,
                                bgcolor="white",
                                style=ft.ButtonStyle(
                                    color={
                                        ft.ControlState.HOVERED: ft.Colors.RED,
                                        ft.ControlState.FOCUSED: "#30419b",
                                        ft.ControlState.DEFAULT: "#30419b"
                                    }
                                ),
                                tooltip="Minimizar"
                            ),
                            ft.IconButton(
                                ft.Icons.CROP_SQUARE,
                                on_click=maximizar,
                                bgcolor="white",
                                style=ft.ButtonStyle(
                                    color={
                                        ft.ControlState.HOVERED: ft.Colors.RED,
                                        ft.ControlState.FOCUSED: "#30419b",
                                        ft.ControlState.DEFAULT: "#30419b"
                                    }
                                ),
                                tooltip="Maximizar"
                            ),
                            ft.IconButton(
                                ft.Icons.CLOSE,
                                on_click=lambda _: page.window.close(),
                                bgcolor="white",
                                style=ft.ButtonStyle(
                                    color={
                                        ft.ControlState.HOVERED: ft.Colors.RED,
                                        ft.ControlState.FOCUSED: "#30419b",
                                        ft.ControlState.DEFAULT: "#30419b"
                                    }
                                ),
                                tooltip="Cerrar"
                            ),
                        ], spacing=0),
                        bgcolor="white", height=63, width=125
                    )
                ], spacing=0),

                # Contenedor desplazable
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=5),
                            ft.Row([
                                ft.Column([
                                    ft.Text("                     PROCESOS INGRESADOS", size=20, weight="bold", color="black"),
                                    ft.Container(height=5),
                                    tabla_procesos,
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                                ft.Column([
                                    ft.Text("                           RESULTADOS", size=20, weight="bold", color="black"),
                                    ft.Container(height=5),
                                    tabla_resultados,
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                            ], vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),

                            ft.Divider(color="#30419b", thickness=3),
                            ft.Row([
                                texto_ejecucion_de_proceso,
                            ], vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([
                                regla
                            ], vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),

                            ft.Row([
                                ft.Container(content=lista_de_progress_bar, width=950, bgcolor="white")
                            ], vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),

                            ft.Row([
                                tabla_medios
                            ], vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        scroll=True,  # Activar desplazamiento
                        expand=True
                    ),
                    bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.WHITE),
                    expand=True,
                    margin=0,
                    padding=0
                )
            ], expand=True, spacing=0)
        ], expand=True, spacing=0)
    )

ft.app(target=main)
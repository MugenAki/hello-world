from django.http import HttpResponse
from django.shortcuts import render, redirect
from bd import models

import os

def hola_mundo(request):
    """ vista con ejemplo de hola mundo """
    html = """
    <html>
        <body>
            <h1>Hola mundo</h1>
        </body>
    </html>
    """
    return HttpResponse(html)


def regresa_elem(listElem):
    cadena="<ul>"
    for elemento in listElem:
        cadena += f"""
            <li>
                {elemento}
            </li>
        """
    cadena += '</ul>'
    return cadena

def regresar_txt():
    listElem=[]
    """regresa archivos de un directorio en terminación .txt"""
    for archivo in os.listdir('C:/Users/jorge/Documents'):
        if (archivo.endswith('.txt')):
            listElem.append(archivo)
    return listElem

def mostrar_plantilla(request):
    """Vista para regresar un html básico"""
    contexto = {'lista': regresar_txt()}
    return render(request, 'vacio.html', contexto)

def formulario_registro(request):
    """Regresa un formulario"""

    t = "formulario.html"
    if request.method == 'GET':
        return render(request, t)
    else: 
        #procesar formulario
        usuario= request.POST.get('usuario', '').strip()
        password= request.POST.get('password', '').strip()
        nombre= request.POST.get('nombre', '').strip()
        edad= request.POST.get('edad', '').strip()
        grupo= request.POST.get('grupo', '').strip()
        errores = validar_valores(usuario=usuario, password=password, nombre=nombre, edad=edad, grupo=grupo)

        if errores:
            c= {'errores': errores}
            return render(request, t, c)
        else:
            nuevo_usr = models.Usuario(usuario=usuario,
                                        password=password,
                                        nombre=nombre,
                                        edad=int(edad),
                                        grupo=grupo)
            nuevo_usr.save()
            request.session['registrado'] = True
            request.session['grupo'] = grupo
            return redirect('/lista/')

def lista_opuestos(request):
    """Muestra la lista de usuarios en el grupo opuesto"""

    registrado = request.session.get('registrado', False)
    grupo = request.session.get('grupo', '')
    if not registrado or not grupo:
        return redirect('/registro/')
    t= 'lista.html'
    grupo_opuesto='A'
    if grupo == 'A':
        grupo_opuesto='B'
    c={'lista': models.Usuario.objects.filter(grupo=grupo_opuesto)}
    return render (request, t, c)

def existe_usuario(usuario):
    """Determina si un usuario existe en la BD"""
    resultado = models.Usuario.objects.filter(usuario=usuario)
    if len(resultado) == 0:
        return False
    else:
        return True

def validar_valores(usuario, password, nombre, edad, grupo):
    """Valida los campos del formulario regresando una lista de errores"""
    errores=[]
    if not usuario:
        errores.append('El usuario está vacío')
    if existe_usuario(usuario):
        errores.append('El usuario ya está registrado')
    if not nombre:
        errores.append('El nombre está vacío')
    if not password:
        errores.append('La contraseña está vacía')
    if not edad.isnumeric():
        errores.append('Edad inválida')
    if not grupo in ['A', 'B']:
        errores.append('El grupo tiene que ser A o B')
    
    return errores
from datetime import datetime
from modelo import (
    Paciente, Medico, Especialidad, Clinica,
    PacienteNoEncontradoException, MedicoNoDisponibleException,
    TurnoOcupadoException, RegistroDuplicadoException,
    RecetaInvalidaException, EspecialidadInvalidaException
)

def menu():
    print("\n--- Menú Clínica ---")
    print("1) Agregar paciente")
    print("2) Agregar médico")
    print("3) Agendar turno")
    print("4) Agregar especialidad a médico")
    print("5) Emitir receta")
    print("6) Ver historia clínica")
    print("7) Ver todos los turnos")
    print("8) Ver todos los pacientes")
    print("9) Ver todos los médicos")
    print("0) Salir")

def main():
    clinica = Clinica()
    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == "1":
                nombre = input("Nombre del paciente: ")
                dni = input("DNI: ")
                fecha_nac = input("Fecha de nacimiento (dd/mm/aaaa): ")
                paciente = Paciente(nombre, dni, fecha_nac)
                clinica.agregar_paciente(paciente)
                print("Paciente registrado correctamente.")
            elif opcion == "2":
                nombre = input("Nombre del médico: ")
                matricula = input("Matrícula: ")
                medico = Medico(nombre, matricula)
                clinica.agregar_medico(medico)
                print("Médico registrado correctamente.")
            elif opcion == "3":
                dni = input("DNI del paciente: ")
                matricula = input("Matrícula del médico: ")
                especialidad = input("Especialidad: ")
                fecha_str = input("Fecha y hora del turno (dd/mm/aaaa HH:MM): ")
                fecha_hora = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
                clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
                print("Turno agendado correctamente.")
            elif opcion == "4":
                matricula = input("Matrícula del médico: ")
                tipo = input("Especialidad: ")
                dias = input("Días de atención (separados por coma, ej: lunes,miércoles): ").split(",")
                medico = clinica.obtener_medico_por_matricula(matricula)
                especialidad = Especialidad(tipo, [d.strip() for d in dias])
                medico.agregar_especialidad(especialidad)
                print("Especialidad agregada correctamente.")
            elif opcion == "5":
                dni = input("DNI del paciente: ")
                matricula = input("Matrícula del médico: ")
                medicamentos = input("Medicamentos (separados por coma): ").split(",")
                clinica.emitir_receta(dni, matricula, [m.strip() for m in medicamentos if m.strip()])
                print("Receta emitida correctamente.")
            elif opcion == "6":
                dni = input("DNI del paciente: ")
                historia = clinica.obtener_historia_clinica(dni)
                print(historia)
            elif opcion == "7":
                turnos = clinica.obtener_turnos()
                if not turnos:
                    print("No hay turnos registrados.")
                else:
                    for t in turnos:
                        print(t)
            elif opcion == "8":
                pacientes = clinica.obtener_pacientes()
                if not pacientes:
                    print("No hay pacientes registrados.")
                else:
                    for p in pacientes:
                        print(p)
            elif opcion == "9":
                medicos = clinica.obtener_medicos()
                if not medicos:
                    print("No hay médicos registrados.")
                else:
                    for m in medicos:
                        print(m)
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except (PacienteNoEncontradoException, MedicoNoDisponibleException, TurnoOcupadoException,
                RegistroDuplicadoException, RecetaInvalidaException, EspecialidadInvalidaException, ValueError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
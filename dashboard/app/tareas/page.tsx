import { getTasks, getTaskStats } from "@/lib/data";
import { CheckSquare, Clock, AlertTriangle, CheckCircle } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function TareasPage() {
  const tasks = await getTasks();
  const stats = await getTaskStats();

  const statusLabels: Record<string, string> = {
    pendiente: "Pendiente", en_progreso: "En progreso", bloqueada: "Bloqueada",
    completada: "Completada", cancelada: "Cancelada",
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Tareas</h1>
        <p className="text-gray-500 mt-1">Gestión de tareas y actividades</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        <div className="card text-center">
          <p className="text-2xl font-bold text-primary-600">{stats.total}</p>
          <p className="text-sm text-gray-500">Total</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
          <p className="text-sm text-gray-500">Pendientes</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-blue-600">{stats.inProgress}</p>
          <p className="text-sm text-gray-500">En progreso</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
          <p className="text-sm text-gray-500">Completadas</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
          <p className="text-sm text-gray-500">Vencidas</p>
        </div>
      </div>

      {/* Completion Rate */}
      {stats.total > 0 && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold mb-4">Tasa de Completado</h2>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-green-500 h-4 rounded-full transition-all"
                  style={{ width: `${stats.completionRate}%` }}
                />
              </div>
            </div>
            <span className="text-lg font-bold text-green-600">{stats.completionRate}%</span>
          </div>
        </div>
      )}

      {/* Tasks List */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Lista de Tareas</h2>
        {tasks.length === 0 ? (
          <div className="text-center py-12">
            <CheckSquare size={48} className="mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500">No hay tareas aún.</p>
            <p className="text-sm text-gray-400 mt-1">
              Habla con Hermes: "Crea una tarea para el proyecto PROJ-001"
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.map((task: any) => {
              const isOverdue = new Date(task.fecha_vencimiento) < new Date() &&
                !["completada", "cancelada"].includes(task.estado);
              return (
                <div key={task.id} className={`flex items-start gap-4 p-4 rounded-lg border ${
                  isOverdue ? "border-red-200 bg-red-50" : "border-gray-200 bg-gray-50"
                }`}>
                  <div className={`mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                    task.estado === "completada"
                      ? "bg-green-500 border-green-500"
                      : "border-gray-300"
                  }`}>
                    {task.estado === "completada" && (
                      <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <p className={`font-medium text-sm ${task.estado === "completada" ? "line-through text-gray-400" : ""}`}>
                        {task.titulo}
                      </p>
                      <span className={`badge ${
                        task.prioridad === "urgente" ? "badge-red" :
                        task.prioridad === "alta" ? "badge-yellow" :
                        task.prioridad === "media" ? "badge-blue" : "badge-gray"
                      }`}>
                        {task.prioridad}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {task.proyecto_id} — Responsable: {task.responsable}
                    </p>
                    <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                      <span className={`flex items-center gap-1 ${isOverdue ? "text-red-600 font-medium" : ""}`}>
                        <Clock size={12} />
                        Vence: {new Date(task.fecha_vencimiento).toLocaleDateString("es-MX")}
                        {isOverdue && " (Vencida)"}
                      </span>
                      <span className={`badge ${
                        task.estado === "completada" ? "badge-green" :
                        task.estado === "en_progreso" ? "badge-blue" :
                        task.estado === "bloqueada" ? "badge-red" : "badge-gray"
                      }`}>
                        {statusLabels[task.estado] || task.estado}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

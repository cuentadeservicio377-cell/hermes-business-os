import { getProjects, getProjectStats } from "@/lib/data";
import { FolderKanban, Calendar, AlertTriangle, CheckCircle } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function ProyectosPage() {
  const projects = await getProjects();
  const stats = await getProjectStats();

  const statusLabels: Record<string, string> = {
    planificado: "Planificado", en_progreso: "En progreso", pausado: "Pausado",
    completado: "Completado", cancelado: "Cancelado", entregado: "Entregado",
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Proyectos</h1>
        <p className="text-gray-500 mt-1">Gestión de proyectos y operaciones</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="card text-center">
          <p className="text-2xl font-bold text-primary-600">{stats.total}</p>
          <p className="text-sm text-gray-500">Total</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-blue-600">{stats.active}</p>
          <p className="text-sm text-gray-500">Activos</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
          <p className="text-sm text-gray-500">Completados</p>
        </div>
        <div className="card text-center">
          <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
          <p className="text-sm text-gray-500">Atrasados</p>
        </div>
      </div>

      {/* Progress Overview */}
      {stats.projects.length > 0 && (
        <div className="card mb-6">
          <h2 className="text-lg font-semibold mb-4">Progreso Promedio</h2>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-primary-600 h-4 rounded-full transition-all"
                  style={{ width: `${stats.avgProgress}%` }}
                />
              </div>
            </div>
            <span className="text-lg font-bold text-primary-600">{stats.avgProgress}%</span>
          </div>
        </div>
      )}

      {/* Projects Grid */}
      <div className="card overflow-x-auto">
        <h2 className="text-lg font-semibold mb-4">Lista de Proyectos</h2>
        {projects.length === 0 ? (
          <div className="text-center py-12">
            <FolderKanban size={48} className="mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500">No hay proyectos aún.</p>
            <p className="text-sm text-gray-400 mt-1">
              Habla con Hermes: "Crea un proyecto nuevo"
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {projects.map((project: any) => {
              const isOverdue = new Date(project.fecha_entrega) < new Date() &&
                ["planificado", "en_progreso", "pausado"].includes(project.estado);
              return (
                <div key={project.id} className={`p-4 rounded-lg border ${isOverdue ? "border-red-200 bg-red-50" : "border-gray-200 bg-gray-50"}`}>
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-semibold text-sm">{project.nombre}</p>
                      <p className="text-xs text-gray-500">{project.id} — {project.cliente_nombre}</p>
                    </div>
                    <span className={`badge ${
                      project.estado === "completado" ? "badge-green" :
                      project.estado === "en_progreso" ? "badge-blue" :
                      project.estado === "pausado" ? "badge-yellow" :
                      project.estado === "cancelado" ? "badge-red" : "badge-gray"
                    }`}>
                      {statusLabels[project.estado] || project.estado}
                    </span>
                  </div>
                  <div className="mt-3">
                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                      <span>Progreso</span>
                      <span>{project.progreso}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${isOverdue ? "bg-red-500" : "bg-primary-600"}`}
                        style={{ width: `${project.progreso}%` }}
                      />
                    </div>
                  </div>
                  <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <Calendar size={12} />
                      <span>Inicio: {new Date(project.fecha_inicio).toLocaleDateString("es-MX")}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Calendar size={12} />
                      <span className={isOverdue ? "text-red-600 font-medium" : ""}>
                        Entrega: {new Date(project.fecha_entrega).toLocaleDateString("es-MX")}
                        {isOverdue && " ⚠️"}
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

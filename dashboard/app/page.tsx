import { getDashboardSummary } from "@/lib/data";
import StatCard from "@/components/StatCard";
import {
  Users,
  TrendingUp,
  FolderKanban,
  CheckSquare,
  AlertTriangle,
  DollarSign,
} from "lucide-react";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const summary = await getDashboardSummary();
  const moneda = summary.company.moneda || "MXN";

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Dashboard — {summary.company.nombre}
        </h1>
        <p className="text-gray-500 mt-1">
          Resumen general de tu negocio
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          title="Total Clientes"
          value={summary.clients.total}
          subtitle={`${Object.values(summary.clients.byStatus).reduce((a: number, b: number) => a + b, 0)} activos`}
          icon={<Users size={24} />}
          color="blue"
        />
        <StatCard
          title="Valor Pipeline"
          value={`${moneda} ${summary.pipeline.totalValue.toLocaleString()}`}
          subtitle={`${summary.pipeline.total} oportunidades`}
          icon={<TrendingUp size={24} />}
          color="green"
        />
        <StatCard
          title="Proyectos Activos"
          value={summary.projects.active}
          subtitle={`${summary.projects.overdue} atrasados`}
          icon={<FolderKanban size={24} />}
          color="purple"
        />
        <StatCard
          title="Tareas Pendientes"
          value={summary.tasks.pending + summary.tasks.inProgress}
          subtitle={`${summary.tasks.overdue} vencidas`}
          icon={<CheckSquare size={24} />}
          color="yellow"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Clientes Recientes</h2>
          {summary.clients.recent.length === 0 ? (
            <p className="text-gray-500 text-sm">No hay clientes registrados aún.</p>
          ) : (
            <div className="space-y-3">
              {summary.clients.recent.map((client: any) => (
                <div key={client.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-sm">{client.nombre}</p>
                    <p className="text-xs text-gray-500">{client.email || "Sin email"}</p>
                  </div>
                  <span className={`badge ${
                    client.estado === "contratado" ? "badge-green" :
                    client.estado === "cotizado" ? "badge-yellow" :
                    client.estado === "lead" ? "badge-gray" : "badge-blue"
                  }`}>
                    {client.estado}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pipeline Overview */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Pipeline de Ventas</h2>
          {summary.pipeline.total === 0 ? (
            <p className="text-gray-500 text-sm">No hay oportunidades en el pipeline.</p>
          ) : (
            <div className="space-y-3">
              {Object.entries(summary.pipeline.byStage).map(([stage, data]: [string, any]) => (
                <div key={stage}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="capitalize font-medium">{stage}</span>
                    <span className="text-gray-500">{data.count} — {moneda} {data.value.toLocaleString()}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{
                        width: `${summary.pipeline.total > 0 ? (data.count / summary.pipeline.total) * 100 : 0}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Projects */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Proyectos</h2>
          {summary.projects.projects.length === 0 ? (
            <p className="text-gray-500 text-sm">No hay proyectos aún.</p>
          ) : (
            <div className="space-y-3">
              {summary.projects.projects.slice(0, 5).map((project: any) => (
                <div key={project.id} className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium text-sm">{project.nombre}</p>
                      <p className="text-xs text-gray-500">{project.cliente_nombre} — {project.id}</p>
                    </div>
                    <span className={`badge ${
                      project.estado === "completado" ? "badge-green" :
                      project.estado === "en_progreso" ? "badge-blue" :
                      project.estado === "pausado" ? "badge-yellow" : "badge-gray"
                    }`}>
                      {project.estado}
                    </span>
                  </div>
                  <div className="mt-2">
                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                      <span>Progreso</span>
                      <span>{project.progreso}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div
                        className="bg-primary-600 h-1.5 rounded-full"
                        style={{ width: `${project.progreso}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Tasks */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Tareas</h2>
          {summary.tasks.tasks.length === 0 ? (
            <p className="text-gray-500 text-sm">No hay tareas aún.</p>
          ) : (
            <div className="space-y-3">
              {summary.tasks.tasks.slice(0, 5).map((task: any) => {
                const isOverdue = new Date(task.fecha_vencimiento) < new Date() &&
                  !["completada", "cancelada"].includes(task.estado);
                return (
                  <div key={task.id} className={`flex items-center justify-between p-3 rounded-lg ${
                    isOverdue ? "bg-red-50" : "bg-gray-50"
                  }`}>
                    <div className="flex items-center gap-3">
                      <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                        task.estado === "completada"
                          ? "bg-green-500 border-green-500"
                          : "border-gray-300"
                      }`}>
                        {task.estado === "completada" && (
                          <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </div>
                      <div>
                        <p className={`text-sm ${task.estado === "completada" ? "line-through text-gray-400" : "font-medium"}`}>
                          {task.titulo}
                        </p>
                        <p className="text-xs text-gray-500">
                          {task.proyecto_id} — Vence: {new Date(task.fecha_vencimiento).toLocaleDateString("es-MX")}
                          {isOverdue && <span className="text-red-600 ml-1 font-medium">⚠️ Vencida</span>}
                        </p>
                      </div>
                    </div>
                    <span className={`badge ${
                      task.prioridad === "urgente" ? "badge-red" :
                      task.prioridad === "alta" ? "badge-yellow" :
                      task.prioridad === "media" ? "badge-blue" : "badge-gray"
                    }`}>
                      {task.prioridad}
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

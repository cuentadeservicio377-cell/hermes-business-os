import { getPipeline, getPipelineSummary } from "@/lib/data";
import { TrendingUp, DollarSign, Users } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function PipelinePage() {
  const entries = await getPipeline();
  const summary = await getPipelineSummary();
  const moneda = "MXN";

  const statusLabels: Record<string, string> = {
    lead: "Lead", prospecto: "Prospecto", cotizado: "Cotizado",
    negociacion: "Negociación", contratado: "Contratado",
    en_produccion: "En producción", completado: "Completado", entregado: "Entregado",
  };

  const statusColors: Record<string, string> = {
    lead: "bg-gray-500", prospecto: "bg-blue-400", cotizado: "bg-yellow-400",
    negociacion: "bg-orange-400", contratado: "bg-green-500",
    en_produccion: "bg-purple-500", completado: "bg-green-600", entregado: "bg-teal-500",
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Pipeline de Ventas</h1>
        <p className="text-gray-500 mt-1">Seguimiento de oportunidades comerciales</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-blue-50 rounded-lg"><Users size={20} className="text-blue-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Total Oportunidades</p>
              <p className="text-2xl font-bold">{summary.total}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-green-50 rounded-lg"><DollarSign size={20} className="text-green-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Valor Total</p>
              <p className="text-2xl font-bold">{moneda} {summary.totalValue.toLocaleString()}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-purple-50 rounded-lg"><TrendingUp size={20} className="text-purple-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Promedio</p>
              <p className="text-2xl font-bold">{moneda} {summary.total > 0 ? Math.round(summary.totalValue / summary.total).toLocaleString() : 0}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-6">Visualización del Pipeline</h2>
        {summary.total === 0 ? (
          <p className="text-gray-500 text-center py-8">No hay datos en el pipeline.</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-2">
            {Object.entries(summary.byStage).map(([stage, data]: [string, any]) => (
              <div key={stage} className="text-center">
                <div className={`${statusColors[stage] || "bg-gray-400"} text-white rounded-t-lg py-2 px-3`}>
                  <p className="text-lg font-bold">{data.count}</p>
                </div>
                <div className="bg-gray-50 rounded-b-lg py-2 px-3 border border-t-0 border-gray-200">
                  <p className="text-xs font-medium capitalize">{statusLabels[stage] || stage}</p>
                  <p className="text-xs text-gray-500 mt-0.5">{moneda} {data.value.toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card overflow-x-auto">
        <h2 className="text-lg font-semibold mb-4">Detalle de Oportunidades</h2>
        {entries.length === 0 ? (
          <div className="text-center py-12">
            <TrendingUp size={48} className="mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500">No hay oportunidades registradas.</p>
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">ID</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Cliente</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Proyecto</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Estado</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Monto</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Fecha</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry: any) => (
                <tr key={entry.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-sm font-mono text-gray-500">{entry.id}</td>
                  <td className="py-3 px-4 text-sm font-medium">{entry.cliente_nombre}</td>
                  <td className="py-3 px-4 text-sm text-gray-600">{entry.proyecto_nombre}</td>
                  <td className="py-3 px-4">
                    <span className={`badge ${
                      entry.estado === "contratado" ? "badge-green" :
                      entry.estado === "cotizado" ? "badge-yellow" :
                      entry.estado === "negociacion" ? "badge-blue" :
                      entry.estado === "lead" ? "badge-gray" : "badge-purple"
                    }`}>
                      {statusLabels[entry.estado] || entry.estado}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm font-medium">{moneda} {entry.monto?.toLocaleString() || 0}</td>
                  <td className="py-3 px-4 text-sm text-gray-500">
                    {new Date(entry.fecha_entrada).toLocaleDateString("es-MX")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

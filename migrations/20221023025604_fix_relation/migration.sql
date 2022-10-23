/*
  Warnings:

  - Made the column `notebook_id` on table `notes` required. This step will fail if there are existing NULL values in that column.

*/
-- DropForeignKey
ALTER TABLE "notes" DROP CONSTRAINT "notes_notebook_id_fkey";

-- AlterTable
ALTER TABLE "notes" ALTER COLUMN "notebook_id" SET NOT NULL;

-- AddForeignKey
ALTER TABLE "notes" ADD CONSTRAINT "notes_notebook_id_fkey" FOREIGN KEY ("notebook_id") REFERENCES "notebooks"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

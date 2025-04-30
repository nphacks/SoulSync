import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { JournalEntryService } from '../../services/journal-entry.service';

@Component({
  selector: 'app-handwritten-journal',
  templateUrl: './handwritten-journal.component.html',
  styleUrl: './handwritten-journal.component.scss'
})
export class HandwrittenJournalComponent {
  previewFiles: any[] = [];
  isSaving = false;
  constructor(private journalEntryService: JournalEntryService, private snackBar: MatSnackBar) {}

  isImage(file: File): boolean {
    return file.type.startsWith('image/');
  }

  getFileIcon(type: string): string {
    if (type.includes('pdf')) return 'picture_as_pdf';
    if (type.includes('word') || type.includes('document')) return 'description';
    return 'insert_drive_file';
  }

  handleFileInput(event: any) {
    const files = event.target.files;
    this.previewFiles = [];
    
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      if (this.isImage(file)) {
        const reader = new FileReader();
        reader.onload = (e: any) => {
          this.previewFiles.push({
            name: file.name,
            type: file.type,
            fileObject: file,
            preview: e.target.result
          });
        };
        reader.readAsDataURL(file);
      } else {
        this.previewFiles.push({
          name: file.name,
          type: file.type,
          fileObject: file
        });
      }
    }
  }

  async submitJournalEntry() {
    if (this.previewFiles.length === 0) return;
  
    this.isSaving = true;
    
    try {
      await Promise.all(
        this.previewFiles.map(fileObj => 
          this.journalEntryService.uploadDocumentEntry(fileObj.fileObject) // Access the File object
        )
      );
      this.snackBar.open('Documents uploaded successfully!', 'Close', { duration: 3000 });
      this.previewFiles = [];
    } catch (error) {
      console.error('Error uploading documents:', error);
      this.snackBar.open('Failed to upload documents', 'Close', { duration: 3000 });
    } finally {
      this.isSaving = false;
    }
  }
}
